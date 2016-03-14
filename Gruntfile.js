module.exports = function(grunt) {

  // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        // copy files as is over to static
        copy: {
            main: {
                files: [{ // fonts
                    expand: true,
                    flatten: true,
                    cwd: 'salt_observer/assets/bower/font-awesome/fonts/',
                    src: '*',
                    dest: 'salt_observer/static/fonts/'
                }]
            },
        },

        // compile less files into css, minified and not minified
        less: {
            dev: {
                options: {
                    paths: ['salt_observer/assets/less'],
                    compress: true
                },
                files: {
                    'salt_observer/static/css/main.css': 'salt_observer/assets/less/main.less'
                }
            }
        },

        // minify js files.
        uglify: {
            jquery: {
                files: {'salt_observer/static/js/jquery.min.js': ['salt_observer/assets/bower/jquery/dist/jquery.js']}
            }
        },
        watch: {
            less: {
                files: ['hshaccounts/assets/**/*.less'],
                tasks: ['less']
            }
        }
    });

    // General Stuff
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // Register tasks here.
    grunt.registerTask('default', ['copy', 'less', 'uglify', 'watch']);

};
