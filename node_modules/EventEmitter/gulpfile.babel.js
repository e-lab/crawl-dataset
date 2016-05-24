import gulp from 'gulp';
import path from 'path';

const join = path.join;
const plugins = require('gulp-load-plugins')({
  scope: ['dependencies']
});

const projectMap = {
  folder: {
    build: '/dist',
    js: '/src'
  },
  file: {
    main_js: 'index.js'
  }
};

function getPath(path) {
  return join(path.type === 'folder' ?  __dirname : '',
    projectMap[path.type][path.name]);
}

const buildPath = getPath({type: 'folder', name: 'build'});
const jsPath = getPath({type: 'folder', name: 'js'});

function compress () {
  let fileName = getPath({type: 'file', name: 'main_js'});

  return gulp.src(join(jsPath, fileName))
    .pipe(plugins.babel())
    .pipe(gulp.dest(buildPath))
      .pipe(plugins.sourcemaps.init())
      .pipe(plugins.rename({
        extname: '.min.js'
      }))
      .pipe(plugins.uglify())
      .pipe(plugins.sourcemaps.write('.'))
      .pipe(gulp.dest(buildPath))
    .pipe(plugins.size({title: 'All JavaScript compressed files (with source maps) have:'}));
};

function lint () {
  return gulp.src([
      join(jsPath, '**/*.js')
    ])
    .pipe(plugins.eslint())
    .pipe(plugins.eslint.format());
};

gulp.task('build', gulp.parallel(compress, lint));
