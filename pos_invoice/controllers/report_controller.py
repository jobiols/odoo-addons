from odoo import http
from odoo.addons.web.controllers.main import ReportController
import json
import time

import werkzeug
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from werkzeug.urls import url_decode, iri_to_uri

from odoo.tools import crop_image, topological_sort, html_escape, pycompat
from odoo.tools.safe_eval import safe_eval
from odoo import http
from odoo.http import content_disposition, dispatch_rpc, request, \
    serialize_exception as _serialize_exception, Response


class ReportControllerAeroo(ReportController):
    """ Cambiamos el data para que salga la factura de aeroo
    """

    @http.route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token):

        import wdb; wdb.set_trace()

        # si no es este reporte funciona como el origial
        original_report = 'point_of_sale.report_invoice'
        if not data.find(original_report):
            return super(ReportControllerAeroo, self).report_download(data, token)

        # le cambiamos el reporte para que salga el de aeroo
        data = data.replace(original_report, 'aeroo_report_ar_einvoice')

        """This function is used by 'qwebactionmanager.js' in order to trigger the download of
        a pdf/controller report.

        :param data: a javascript array JSON.stringified containg report internal url ([0]) and
        type [1]
        :returns: Response with a filetoken cookie and an attachment header
        """
        requestcontent = json.loads(data)
        url, type = requestcontent[0], requestcontent[1]
        try:
            if type == 'qweb-pdf':
                reportname = url.split('/report/pdf/')[1].split('?')[0]

                docids = None
                if '/' in reportname:
                    reportname, docids = reportname.split('/')

                # forzamos un id de factura
                docids = '200'

                if docids:
                    # Generic report:
                    response = self.report_routes(reportname, docids=docids,
                                                  converter='pdf')
                else:
                    # Particular report:
                    data = url_decode(url.split('?')[
                                          1]).items()  # decoding the args represented in JSON
                    response = self.report_routes(reportname, converter='pdf',
                                                  **dict(data))

                report = request.env[
                    'ir.actions.report']._get_report_from_name(reportname)
                filename = "%s.%s" % (report.name, "pdf")
                if docids:
                    ids = [int(x) for x in docids.split(",")]
                    obj = request.env[report.model].browse(ids)
                    if report.print_report_name and not len(obj) > 1:
                        report_name = safe_eval(report.print_report_name,
                                                {'object': obj, 'time': time})
                        filename = "%s.%s" % (report_name, "pdf")
                response.headers.add('Content-Disposition',
                                     content_disposition(filename))
                response.set_cookie('fileToken', token)
                return response
            else:
                return
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))

    @http.route([
        '/report/<converter>/<reportname>',
        '/report/<converter>/<reportname>/<docids>',
    ], type='http', auth='user', website=True)
    def report_routes(self, reportname, docids=None, converter=None, **data):

        report = request.env['ir.actions.report']._get_report_from_name(reportname)
        context = dict(request.env.context)

        if docids:
            docids = [int(i) for i in docids.split(',')]
        if data.get('options'):
            data.update(json.loads(data.pop('options')))
        if data.get('context'):
            # Ignore 'lang' here, because the context in data is the one from the webclient *but* if
            # the user explicitely wants to change the lang, this mechanism overwrites it.
            data['context'] = json.loads(data['context'])
            if data['context'].get('lang'):
                del data['context']['lang']
            context.update(data['context'])
        if converter == 'html':
            html = report.with_context(context).render_aeroo(docids, data=data)[0]
            return request.make_response(html)
        elif converter == 'pdf':
            pdf = report.with_context(context).render_aeroo(docids, data=data)[0]
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            raise werkzeug.exceptions.HTTPException(description='Converter %s not implemented.' % converter)
