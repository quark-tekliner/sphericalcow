require('./scoreboard/controllers/index.coffee')

app = angular.module('scoreboardApp', [
    'scoreboardControllers'
])
