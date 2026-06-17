const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const config = getDefaultConfig(__dirname);

// Force axios to use browser build
config.resolver.resolveRequest = (context, moduleName, platform) => {
  if (moduleName === 'axios' || moduleName.startsWith('axios/')) {
    // Force browser build of axios
    return {
      filePath: path.resolve(__dirname, 'node_modules/axios/dist/browser/axios.cjs'),
      type: 'sourceFile',
    };
  }
  
  // Default resolver
  return context.resolveRequest(context, moduleName, platform);
};

module.exports = config;
