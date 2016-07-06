module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        less: {
            production: {
                options: {
                    paths: [
                        'assets/css',
                        'bower_components/'
                    ],
                    sourceMap: true
                },
                files: {
                    'common/static/app.css': 'assets/css/app.less'
                }
            }
        },
        concat: {
            js: {
                src: [
                    'bower_components/jquery/dist/jquery.js',
                    'bower_components/bootstrap/dist/js/bootstrap.js',
                    'assets/js/*.js'
                ],
                dest: 'common/static/app.js'
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-concat');
}
