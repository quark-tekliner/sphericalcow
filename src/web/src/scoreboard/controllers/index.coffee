angular.module('scoreboardControllers', [])
    .controller('Scoreboard', [
        '$scope'
        '$http'
        require('./scoreboard.coffee')
    ])
