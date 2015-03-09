(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
angular.module('scoreboardControllers', []).controller('Scoreboard', ['$scope', '$http', require('./scoreboard.coffee')]);



},{"./scoreboard.coffee":2}],2:[function(require,module,exports){
var Scoreboard;

Scoreboard = (function() {
  function Scoreboard($scope, $http) {
    this.$scope = $scope;
    this.$http = $http;
    this._loadScoreboard();
  }

  Scoreboard.prototype._loadScoreboard = function() {
    return this.$http.get('/scoreboard').success((function(_this) {
      return function(data, status, headers, config) {
        return _this._renderScoreboard(data);
      };
    })(this)).error((function(_this) {
      return function(data, status, headers, config) {
        return _this._rendererror(data);
      };
    })(this));
  };

  Scoreboard.prototype._renderScoreboard = function(users) {
    return this.$scope.users = users;
  };

  Scoreboard.prototype._renderError = function(err) {
    return console.error(err);
  };

  return Scoreboard;

})();

module.exports = Scoreboard;



},{}],3:[function(require,module,exports){
var app;

require('./scoreboard/controllers/index.coffee');

app = angular.module('scoreboardApp', ['scoreboardControllers']);



},{"./scoreboard/controllers/index.coffee":1}]},{},[3]);
