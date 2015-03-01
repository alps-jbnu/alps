var Register = function() {

	"use strict";

	var renderStudentCheckBox = function() {
		var checkbox = $("input[name='jbnu_student']");
		if (checkbox.is(':checked')) {
			$("div.jbnu").removeClass('hidden');
		} else {
			$('div.jbnu').addClass('hidden');
		}
	};

	var initStudentCheckBox = function() {
		var checkbox = $("input[name='jbnu_student']");
		checkbox.change(function() {
			renderStudentCheckBox();
		});
	};

	return {
		init: function() {
			initStudentCheckBox();
			renderStudentCheckBox();
		}
	};
}();