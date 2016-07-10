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
                    'common/static/_app.css': 'assets/css/app.less'
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
            },
            css: {
                src: [
                    'bower_components/normalize-css/normalize.css',
                    'common/static/_app.css'
                ],
                dest: 'common/static/app.css'
            }
        },
        clean: {
            temp_assets: ['common/static/_app.*']
        },
        watch: {
            css: {
                files: ['assets/css/*.less'],
                tasks: ['assets:css']
            },
            js: {
                files: ['assets/js/*.js'],
                tasks: ['assets:js']
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('assets:css', 'compile CSS assets',
        ['less:production', 'concat:css', 'clean:temp_assets']);
    grunt.registerTask('assets:js', 'compile JS assets',
        ['concat:js']);
}
