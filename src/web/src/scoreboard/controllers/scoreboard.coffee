class Scoreboard

    constructor: (@$scope, @$http) ->
        @_loadScoreboard()

    _loadScoreboard: () ->
        @$http.get('/scoreboard')
            .success((data, status, headers, config) => @_renderScoreboard(data))
            .error((data, status, headers, config) => @_rendererror(data))

    _renderScoreboard: (users) ->
        @$scope.users = users

    _renderError: (err) ->
        console.error(err)

module.exports = Scoreboard
