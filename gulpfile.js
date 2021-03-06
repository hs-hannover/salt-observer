var gulp = require('gulp');
var plugins = require('gulp-load-plugins')();

var src = './salt_observer/assets/'
var dst = './salt_observer/static/'

// Every available task

gulp.task('compile:less', compileLess);
gulp.task('collect:images', collectImages);
gulp.task('collect:fonts', collectFonts);
gulp.task('build:javascript:contrib', buildJavascriptContrib);
gulp.task('build:javascript:custom', buildJavascriptCustom);
gulp.task('build:javascript', [
    'build:javascript:contrib',
    'build:javascript:custom']
);
gulp.task('default', [
    'build:javascript',
    'collect:images',
    'collect:fonts',
    'compile:less'
]);
gulp.task('build', ['default'])

gulp.task('watch', ['default'], function() {
    var less_watcher = gulp.watch(src + 'less/**/*.less', ['compile:less']);
    var img_watcher = gulp.watch(src + 'img/**/*', ['collect:images']);
    var js_watcher = gulp.watch(src + 'js/**/*.js', ['build:javascript:custom']);
});

// Actually the tasks

function compileLess() {
    return gulp.src(src + 'less/_init.less')
        .pipe(plugins.less())
        .pipe(plugins.cssmin())
        .pipe(plugins.rename('main.min.css'))
        .pipe(gulp.dest(dst + 'css'));
};

function collectImages() {
    return gulp.src(src + 'img/**/*').pipe(gulp.dest(dst + 'img'));
};

function collectFonts() {
    return gulp.src('node_modules/font-awesome/fonts/*').pipe(gulp.dest(dst + 'fonts'))
};

function buildJavascriptContrib() {
    return gulp.src([
        'jquery/dist/jquery.js',
        'bootstrap/dist/js/bootstrap.js',
        'tablesorter/dist/js/jquery.tablesorter.combined.js',
        'filtertable/jquery.filtertable.js',
        'jdenticon/dist/jdenticon.js',
        'vis/dist/vis.js',
    ], {cwd: 'node_modules'})
        .pipe(plugins.concat('main.js'))
        .pipe(gulp.dest(dst + 'js/contrib'))
        .pipe(plugins.uglify())
        .pipe(plugins.rename({suffix: '.min'}))
        .pipe(gulp.dest(dst + 'js/contrib'))
}

function buildJavascriptCustom() {
    return gulp.src(src + 'js/**/*')
        .pipe(gulp.dest(dst + 'js'))
        .pipe(plugins.uglify().on('error', handleError))
        .pipe(plugins.rename({suffix: '.min'}))
        .pipe(gulp.dest(dst + 'js'))
};

function cleanup() {
    gulp.src(dst, {read: false}).pipe(plugins.clean())
};

function handleError(err) {
    console.log('[\033[31mCritical\033[0m] Line '+err.lineNumber+' in '+err.message);
    this.emit('end');
}
