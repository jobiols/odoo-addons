
// this module interfaces with the barcode reader. It assumes the barcode reader
// is set-up to act like  a keyboard. Use connect() and disconnect() to activate
// and deactivate the barcode reader. Use set_action_callbacks to tell it
// what to do when it reads a barcode.
var BarcodeReader = core.Class.extend({

    scan: function(code){
        if (!code) {
            return;
        }
        var parsed_result = this.barcode_parser.parse_barcode(code);

        // hay que sacarle el ultimo digito al base_code, (?) que loco...
        var aa = parsed_result.base_code / 10
        parsed_result.base_code = Math.trunc(aa)

        if (this.action_callback[parsed_result.type]) {
            this.action_callback[parsed_result.type](parsed_result);
        } else if (this.action_callback.error) {
            this.action_callback.error(parsed_result);
        } else {
            console.warn("Ignored Barcode Scan:", parsed_result);
        }
    },

});

