var WritingPost = function() {

    "use strict";

    var getEditorContentOnSubmit = function(editor) {
        var textarea = $('#post_content');
        var form = $('#edit-form');

        form.submit(function(event) {
            textarea.val(editor.getSession().getValue());
            return true;
        });
    };

    var getEditorContentOnLoad = function(editor) {
        var textarea = $('#post_content');

        $(document).ready(function() {
            editor.$blockScrolling = Infinity;
            editor.setValue(textarea.val(), 1);
        });
    };

    return {
        init: function(editor) {
            getEditorContentOnSubmit(editor);
            getEditorContentOnLoad(editor);
        }
    };
}();
