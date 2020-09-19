const gulp = require('gulp');
const sass = require('gulp-sass');
const cleanCSS = require('gulp-clean-css');
const sourcemaps = require('gulp-sourcemaps');
const autoprefixer = require('gulp-autoprefixer');
const browserSync = require('browser-sync').create();

const paths = {
  styles: {
    src: './app/static/scss/**/*.scss',
    dest: './app/static/css'
  }
}

//compile scss into css
const style = () => {
  const { styles : { src, dest }} = paths;
  // 1. where is scss file
  return gulp.src(src)
  // 2. pass that file through sass compiler
    .pipe(sass())
    .on("error", sass.logError)
  // 3. provide auto-prefixing to support multiple browsers
    .pipe(autoprefixer({
      cascade: false
    })) 
  // 4. where to save compiled CSS
    .pipe(gulp.dest(dest))
  // 5. minify CSS
    .pipe(cleanCSS())
    .pipe(gulp.dest(dest))
  // 6. stream changes to all browsers
    .pipe(browserSync.stream());
}

const watch = () => {
  // sets up watcher to reload pages on scss compile
  browserSync.init({
    // provide proxy address to watch
    proxy: "localhost:5000",
    // optionally provide ["browser_name", "browser_name"]
    browser: "google chrome"
  });

  // shcedule tasks
  gulp.watch('./app/static/**/*.scss', style);

  // This will reload browser and update HTML files
  // gulp.watch('./app/templates/**/*.html').on('change', browserSync.reload);

  gulp.watch('./static/js/**/*.js').on('change', browserSync.reload);

}

exports.style = style;
exports.watch = watch;
