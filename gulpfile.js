const gulp = require('gulp');                         // main module
const sass = require('gulp-sass');                    // sass files compiler
const autoprefixer = require('gulp-autoprefixer');    // prefixing of css styles for older browsers
const cleanCSS = require('gulp-clean-css');           // minify css
const plumber = require('gulp-plumber');              // error handler
const browserSync = require('browser-sync').create(); // browser reloader

const paths = {
  styles: {
    src: './scss/**/*.scss',
    dest: './app/static/css'
  }
}

const style = () => {
  const { styles : { src, dest }} = paths;

  return gulp.src(src)
    .pipe(plumber())              // set up error handling
    .pipe(sass())                 // pass files through sass compiler
    .on("error", sass.logError)
    .pipe(autoprefixer({
      cascade: false
    }))                           // enable auto-prefixing
    .pipe(gulp.dest(dest))        // save compiled css to dest folder
    // .pipe(cleanCSS())          // minify css (optional)
    // .pipe(gulp.dest(dest))
    .pipe(browserSync.stream());  // update browser
}

const watch = () => {
  browserSync.init({
    notify: false,                // turn off sync notification
    proxy: "localhost:5000",      // provide address to watch
    // select multiple browsers ["browser_name", "browser_name"]
    browser: "chrome"
  });

  gulp.watch('./scss/**/*.scss', style);                                // reload browser on CSS update
  gulp.watch('./app/templates/**/*.html').on('change', browserSync.reload);   // reload browser on HTML update
  gulp.watch('./static/js/**/*.js').on('change', browserSync.reload);         // reload browser on JS update
}

exports.style = style;
exports.watch = watch;
