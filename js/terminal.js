/*eslint quote-props: ["error", "always"]*/

function tcv(c) {
	var tcvTerm = document.getElementById('terminal');
	var tcvInput = document.createElement('textarea');
	var tcvDisplay = c.motd || 'Default Terminal';
	var tcvApp = c.app || {};
	var tcvTempInput = '';
	var tcvTempInput2 = [];
	var tcvPrompt = c.prompt || '> ';
	var tcvCommands = c.cmd || { "help": help, "clear": clear, "run": run };
	var tcvTags = [
		'black',
		'red',
		'green',
		'yellow',
		'blue',
		'magenta',
		'cyan',
		'white',
		'bold'
	];

	tcvInput.className = 'tcv-input';
	document.body.appendChild(tcvInput);
	tcvInput.focus();

	function showTerm() {
		var cursor = '<span class="cursor"></span>';
		tcvTerm.innerHTML = tcvDisplay + tcvPrompt;
		if (tcvTempInput2.length) {
			tcvTerm.innerHTML += renderDisplay(tcvTempInput2.join(' ')) + ' ';
		}
		tcvTerm.innerHTML += tcvTempInput + cursor;
	}

	function renderDisplay(str) {
		var str;
		for (i = 0; i < tcvTags.length; i++) {
			var start = new RegExp('{' + tcvTags[i] + '}', 'g');
			var end = new RegExp('{/' + tcvTags[i] + '}', 'g');
			str = str.replace(start, '<span class="' + tcvTags[i] + '">');
			str = str.replace(end, '</span>');
		}
		return str;
	}

	function sanitize(str, rep) {
		var str;
		for (i = 0; i < tcvTags.length; i++) {
			var start = new RegExp('{' + tcvTags[i] + '}', 'g');
			var end = new RegExp('{/' + tcvTags[i] + '}', 'g');
			str = str.replace(start, '');
			str = str.replace(end, '');
		}
		return str;
	}

	function processInput() {
		var displayOutput;
		var input = tcvTempInput;
		tcvTempInput2.push(input);
		var splitInput = tcvTempInput2;
		var cmd = sanitize(splitInput[0]);
		tcvDisplay += tcvPrompt + renderDisplay(tcvTempInput2.join(' '));
		tcvTempInput = '';
		tcvTempInput2 = [];
		if (cmd != '') {
			if (!tcvCommands.hasOwnProperty(cmd)) {
				displayOutput =
					'\t{red}//{bold}' +
					cmd +
					'{/bold}: is not a command{/red}\n';
			} else {
				displayOutput = tcvCommands[cmd](splitInput, splitInput.length);
			}
			if (displayOutput === false) {
				displayOutput =
					'\t{red}//{bold}' +
					cmd +
					'{/bold}: is not a command{/red}\n';
			}
			displayOutput = renderDisplay(displayOutput);
			tcvDisplay += displayOutput;
		} else
			tcvDisplay += renderDisplay('{white}//help, run, clear{/white}\n');
		showTerm();
	}

	function help() {
		return '\t{white}//enter the command:{/white}{magenta} run textwars{/magenta}\n';
	}

	function clear() {
		tcvDisplay = '';
		return '';
	}

	function run(input, args) {
		var app = input[1];
		if (app != '' && tcvApp.hasOwnProperty(app)) {
			return tcvApp[app]();
		} else if (app != '' && !tcvApp.hasOwnProperty(app)) {
			return '\t{white}//Application not found{/white}\n';
		} else {
			return "\t{white}//you didn't specify an application to run{/white}\n";
		}
	}

	function colorize() {
		if (tcvTempInput2.length == 0) {
			tcvTempInput2.push('{cyan}' + tcvTempInput + '{/cyan}');
		} else tcvTempInput2.push(tcvTempInput);
		tcvTempInput = '';
	}

	function promptInput(e) {
		e.preventDefault();
		tcvInput.value = '';

		if (e.which >= 48 && e.which <= 90) {
			tcvTempInput += e.key;
		} else if (e.which == 32) {
			colorize();
		} else if (e.which == 13) {
			colorize();
			processInput();
		} else if (e.which == 8) {
			if (tcvTempInput != '') {
				tcvTempInput = tcvTempInput.substr(0, tcvTempInput.length - 1);
			}
			if (tcvTempInput2 != '' && tcvTempInput == '') {
				tcvTempInput = tcvTempInput2.splice(-1);
				tcvTempInput = sanitize(tcvTempInput.join());
			}
		}
		showTerm();
	}

	tcvInput.addEventListener('keydown', promptInput);
	tcvTerm.addEventListener('click', function(e) {
		e.preventDefault();
		tcvInput.focus();
	});
	showTerm();
}
