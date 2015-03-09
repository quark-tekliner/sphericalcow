class Polls

    constructor: (@$scope, @$http) ->
        @_loadPolls()

    _loadPolls: () ->
        @$scope.loading = true
        @$http.get('/polls')
            .success((data, status, headers, config) => @_renderPolls(data))
            .error((data, status, headers, config) => @_renderError(data))

    _renderPolls: (polls) ->
        @$scope.loading = false
        for poll in polls
            for answer in poll.answers
                answer.isIncorrect = true if answer.id == poll.problem_is_incorrect_answer_id
                answer.isCorrect = true if answer.id == poll.correct_answer_id
        @$scope.polls = polls

    _renderError: (err) ->
        @$scope.loading = false
        @$scope.pollsLoadingError = true
        console.error(err)

    markAnswerAsCorrect: (poll, answer) ->
        answer.isIncorrect = false
        @_clearAnswersState(poll, 'isCorrect')
        answer.isCorrect = true
        @_setCanSave(poll)

    markAnswerAsIncorrect: (poll, answer) ->
        answer.isCorrect = false
        @_clearAnswersState(poll, 'isIncorrect')
        answer.isIncorrect = true
        @_setCanSave(poll)

    _clearAnswersState: (poll, state) ->
        answer[state] = false for answer in poll.answers

    onFactorChange: (poll) ->
        @_setCanSave(poll)

    _setCanSave: (poll) ->
        if not poll.factor or not poll.factor.length
            return poll.canSave = false
        isCorrectPresent = false
        isIncorrectPresent = false
        for answer in poll.answers
            isCorrectPresent = true if answer.isCorrect
            isIncorrectPresent = true if answer.isIncorrect
        poll.canSave = isCorrectPresent and isIncorrectPresent

    save: (poll) ->
        correct_answer_id=null
        problem_is_incorrect_answer_id=null
        for answer in poll.answers
            correct_answer_id = answer.id if answer.isCorrect
            problem_is_incorrect_answer_id = answer.id if answer.isIncorrect
        @$http.post("/polls/#{poll.id}", {
            factor: poll.factor
            correct_answer_id
            problem_is_incorrect_answer_id
        })
        .success(() ->)
        .error(() ->)


module.exports = Polls
