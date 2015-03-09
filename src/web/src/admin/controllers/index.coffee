angular.module('adminControllers', [])
    .controller('Polls', [
        '$scope'
        '$http'
        require('./polls.coffee')
    ])
