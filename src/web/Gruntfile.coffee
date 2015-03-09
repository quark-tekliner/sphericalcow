module.exports = (grunt) ->
    grunt.initConfig
        pkg: grunt.file.readJSON('package.json')
        browserify:
            main:
                files:
                    'static/js/calculus_admin_app.js': ['src/calculus_admin_app.coffee']
                    'static/js/scoreboard_app.js': ['src/scoreboard_app.coffee']
                options:
                    transform: ['coffeeify']

        watch:
            src:
                files: ['src/**/*.coffee']
                tasks: ['browserify']
            #css:


    grunt.loadNpmTasks('grunt-browserify')
    grunt.loadNpmTasks('grunt-contrib-watch')

    grunt.registerTask('build', ['browserify'])
