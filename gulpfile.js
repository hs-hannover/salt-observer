var gulp = require('gulp');
var plugins = require('gulp-load-plugins')();

var src = './salt_observer/assets/'
var dst = './salt_observer/static/'

// Every available task

gulp.task('compile:less', compileLess);
gulp.task('collect:images', collectImages);
gulp.task('collect:fonts', collectFonts);
gulp.task('build:contrib-javascript', buildContribJavascript);
gulp.task('build:custom-javascript', buildCustomJavascript);
gulp.task('cleanup', cleanup);

gulp.task('default', [
    'compile:less',
    'collect:images',
    'collect:fonts',
    'build:contrib-javascript',
    'build:custom-javascript'
]);

// gulp.task('watch', ['default'], function() {
//     var less_watcher = gulp.watch(src + 'less/**/*.less', ['compileLess']);
//     var js_watcher = gulp.watch(src + 'js/main.js', ['buildMainJavascript']);
//     var js_watcher = gulp.watch(['js/**/*.js', '!js/main.js'], {cwd: src}, ['buildCustomJavascript']);
// });

// Actually the tasks

function compileLess() {
    return gulp.src(src + 'less/main.less')
        .pipe(plugins.less())
        .pipe(plugins.cssmin())
        .pipe(plugins.rename({suffix: '.min'}))
        .pipe(gulp.dest(dst + 'css'));
};

function collectImages() {
    return gulp.src(src + 'img/**/*').pipe(gulp.dest(dst + 'img'));
};

function collectFonts() {
    return gulp.src('node_modules/font-awesome/fonts/*').pipe(gulp.dest(dst + 'fonts'))
};

function buildContribJavascript() {
    return gulp.src([
        'jquery/dist/jquery.js',
        'bootstrap/dist/js/bootstrap.js',
        'tablesorter/dist/js/jquery.tablesorter.combined.js',
        'filtertable/jquery.filtertable.js'
    ], {cwd: 'node_modules'})
        .pipe(plugins.uglify())
        .pipe(plugins.concat('main.min.js'))
        .pipe(gulp.dest(dst + 'js/contrib'))
};

function buildCustomJavascript() {
    return gulp.src(src + 'js/**/*')
        .pipe(plugins.uglify())
        .pipe(plugins.rename({suffix: '.min'}))
        .pipe(gulp.dest(dst + 'js'))
};

function cleanup() {
    gulp.src(dst, {read: false}).pipe(plugins.clean())
};
