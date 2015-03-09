(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
angular.module('adminControllers', []).controller('Polls', ['$scope', '$http', require('./polls.coffee')]);



},{"./polls.coffee":2}],2:[function(require,module,exports){
var Polls;

Polls = (function() {
  function Polls($scope, $http) {
    this.$scope = $scope;
    this.$http = $http;
    this._loadPolls();
  }

  Polls.prototype._loadPolls = function() {
    this.$scope.loading = true;
    return this.$http.get('/polls').success((function(_this) {
      return function(data, status, headers, config) {
        return _this._renderPolls(data);
      };
    })(this)).error((function(_this) {
      return function(data, status, headers, config) {
        return _this._renderError(data);
      };
    })(this));
  };

  Polls.prototype._renderPolls = function(polls) {
    var answer, i, j, len, len1, poll, ref;
    this.$scope.loading = false;
    for (i = 0, len = polls.length; i < len; i++) {
      poll = polls[i];
      ref = poll.answers;
      for (j = 0, len1 = ref.length; j < len1; j++) {
        answer = ref[j];
        if (answer.id === poll.problem_is_incorrect_answer_id) {
          answer.isIncorrect = true;
        }
        if (answer.id === poll.correct_answer_id) {
          answer.isCorrect = true;
        }
      }
    }
    return this.$scope.polls = polls;
  };

  Polls.prototype._renderError = function(err) {
    this.$scope.loading = false;
    this.$scope.pollsLoadingError = true;
    return console.error(err);
  };

  Polls.prototype.markAnswerAsCorrect = function(poll, answer) {
    answer.isIncorrect = false;
    this._clearAnswersState(poll, 'isCorrect');
    answer.isCorrect = true;
    return this._setCanSave(poll);
  };

  Polls.prototype.markAnswerAsIncorrect = function(poll, answer) {
    answer.isCorrect = false;
    this._clearAnswersState(poll, 'isIncorrect');
    answer.isIncorrect = true;
    return this._setCanSave(poll);
  };

  Polls.prototype._clearAnswersState = function(poll, state) {
    var answer, i, len, ref, results;
    ref = poll.answers;
    results = [];
    for (i = 0, len = ref.length; i < len; i++) {
      answer = ref[i];
      results.push(answer[state] = false);
    }
    return results;
  };

  Polls.prototype.onFactorChange = function(poll) {
    return this._setCanSave(poll);
  };

  Polls.prototype._setCanSave = function(poll) {
    var answer, i, isCorrectPresent, isIncorrectPresent, len, ref;
    if (!poll.factor || !poll.factor.length) {
      return poll.canSave = false;
    }
    isCorrectPresent = false;
    isIncorrectPresent = false;
    ref = poll.answers;
    for (i = 0, len = ref.length; i < len; i++) {
      answer = ref[i];
      if (answer.isCorrect) {
        isCorrectPresent = true;
      }
      if (answer.isIncorrect) {
        isIncorrectPresent = true;
      }
    }
    return poll.canSave = isCorrectPresent && isIncorrectPresent;
  };

  Polls.prototype.save = function(poll) {
    var answer, correct_answer_id, i, len, problem_is_incorrect_answer_id, ref;
    correct_answer_id = null;
    problem_is_incorrect_answer_id = null;
    ref = poll.answers;
    for (i = 0, len = ref.length; i < len; i++) {
      answer = ref[i];
      if (answer.isCorrect) {
        correct_answer_id = answer.id;
      }
      if (answer.isIncorrect) {
        problem_is_incorrect_answer_id = answer.id;
      }
    }
    return this.$http.post("/polls/" + poll.id, {
      factor: poll.factor,
      correct_answer_id: correct_answer_id,
      problem_is_incorrect_answer_id: problem_is_incorrect_answer_id
    }).success(function() {}).error(function() {});
  };

  return Polls;

})();

module.exports = Polls;



},{}],3:[function(require,module,exports){
var app;

require('./admin/controllers/index.coffee');

app = angular.module('calculusAdminApp', ['adminControllers']);



},{"./admin/controllers/index.coffee":1}]},{},[3]);
