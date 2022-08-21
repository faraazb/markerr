/**
 * From Preact documentation
 * 
 * Function that mutates the original webpack config.
 * Supports asynchronous changes when a promise is returned (or it's an async function).
 *
 * @param {import('preact-cli').Config} config - original webpack config
 * @param {import('preact-cli').Env} env - current environment and options pass to the CLI
 * @param {import('preact-cli').Helpers} helpers - object with useful helpers for working with the webpack config
 * @param {Record<string, unknown>} options - this is mainly relevant for plugins (will always be empty in the config), default to an empty object
 */
export default (config, env, helpers, options) => {
	/** to include other dircetories when using CSS modules **/
	// config.module.rules[4].include = [
	// 	path.resolve(__dirname, 'src', 'annotator'),
	// 	path.resolve(__dirname, 'src', 'components')
	//   ];
	  
	// config.module.rules[5].exclude = [
	//   path.resolve(__dirname, 'src', 'annotator'),
	//   path.resolve(__dirname, 'src', 'components')
	// ];

	// need to undertsand how CSS modules and microbundle work together
	let css = helpers.getLoadersByName(config, 'css-loader')[0];
	css.loader.options.modules = false;
};
