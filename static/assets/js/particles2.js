/* -----------------------------------------------
/* Author : Vincent Garreau  - vincentgarreau.com
/* MIT license: http://opensource.org/licenses/MIT
/* Demo / Generator : vincentgarreau.com/particles.js
/* GitHub : github.com/VincentGarreau/particles.js
/* How to use? : Check the GitHub README
/* v2.0.0
/* ----------------------------------------------- */


/* ---------- global functions - vendors ------------ */

window.particlesJS = function(tag_id, params){

    /* pJS elements */
    var pJS_tag = document.getElementById(tag_id),
        pJS_canvas_class = '',
        exist_canvas = pJS_tag.getElementsByClassName(pJS_canvas_class);
  
    /* remove canvas if exists into the pJS target tag */
    if(exist_canvas.length){
      while(exist_canvas.length > 0){
        pJS_tag.removeChild(exist_canvas[0]);
      }
    }
  
    /* create canvas element */
    var canvas_el = document.createElement('canvas');
    canvas_el.className = pJS_canvas_class;
  
    /* append canvas */
    var canvas = document.getElementById(tag_id).appendChild(canvas_el);
  
  
  
  };
  