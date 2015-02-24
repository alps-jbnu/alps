var Register = function() {

	"use strict";

	var initStudentCheckBox = function() {
		var checkbox = $("input[name='jbnu-student']");
		checkbox.change(function() {
			if (checkbox.is(':checked')) {
				console.log('checked');
				$("div.jbnu").removeClass('hidden');
			} else {
				console.log('not checked');
				$('div.jbnu').addClass('hidden');
			}
		});
	};

	return {
		init: function() {
			initStudentCheckBox();
		}
	};
}();