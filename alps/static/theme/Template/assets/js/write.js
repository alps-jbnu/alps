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

    return {
        init: function(editor) {
            getEditorContentOnSubmit(editor);
        }
    };
}();
