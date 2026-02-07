const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// Exclude Node.js core modules - axios will use its browser build automatically
config.resolver.extraNodeModules = {
  crypto: false,
  stream: false,
  http: false,
  https: false,
  os: false,
  url: false,
  zlib: false,
  path: false,
  fs: false,
  net: false,
  tls: false,
};

module.exports = config;
