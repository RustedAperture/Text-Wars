/*eslint quote-props: ["error", "always"]*/

function textwars() {
	var test1 = new tcv({
		"motd": 'Textwars&copy 2019 | Cameron Varley (camvar97)\n',
		"cmd": { "exit": init }
	});
}

function init() {
	var test = new tcv({
		"motd": 'Welcome to the javascript port of my game\n',
		"app": {
			"textwars": textwars
		}
	});
}

init();
