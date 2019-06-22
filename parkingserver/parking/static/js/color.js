var style = getComputedStyle(document.body);

let root = document.documentElement;

var maincolor = chroma(style.getPropertyValue('--mdc-theme-primary'))
var secondarycolor = chroma(style.getPropertyValue('--mdc-theme-secondary'))
var surfacecolor = chroma(style.getPropertyValue('--mdc-theme-surface'))
var backgroundcolor = chroma(style.getPropertyValue('--mdc-theme-background'))
var colors = [];
var s;

root.style.setProperty('--mdc-theme-on-primary',maincolor.get('lab.l') < 70 ? maincolor.brighten(4) : maincolor.darken(4));
root.style.setProperty('--mdc-theme-on-secondary',secondarycolor.get('lab.l') < 70 ? secondarycolor.brighten(4) : secondarycolor.darken(4));
root.style.setProperty('--mdc-theme-on-surface',surfacecolor.get('lab.l') < 70 ? surfacecolor.brighten(4) : surfacecolor.darken(4));
root.style.setProperty('--mdc-theme-on-background',backgroundcolor.get('lab.l') < 70 ? backgroundcolor.brighten(4) : backgroundcolor.darken(4));

$.post("/getcolors",{'csrfmiddlewaretoken': csrftoken},function(data){
    console.log(data.success);
    console.log(data.colors);
    colors = data.colors;
    s = data.success;
    if (s){
        root.style.setProperty('--mdc-theme-primary',colors[0]);
        root.style.setProperty('--mdc-theme-secondary',colors[1]);
        //root.style.setProperty('--mdc-theme-surface',((chroma(colors[0]).get('lab.l') < 70 ? maincolor.brighten(2) : maincolor.darken(2))).saturate(3));
        //root.style.setProperty('--mdc-theme-background',((chroma(colors[1]).get('lab.l') < 70 ? secondarycolor.brighten(2) : secondarycolor.darken(2))).saturate(3));
        root.style.setProperty('--mdc-theme-on-primary',((chroma(colors[0]).get('lab.l') < 70 ? maincolor.brighten(4) : maincolor.darken(4))).desaturate(2));
        root.style.setProperty('--mdc-theme-on-secondary',chroma(colors[1]).get('lab.l') < 70 ? secondarycolor.brighten(4) : secondarycolor.darken(4));
        root.style.setProperty('--mdc-theme-on-surface',surfacecolor.get('lab.l') < 70 ? surfacecolor.brighten(4) : surfacecolor.darken(4));
        root.style.setProperty('--mdc-theme-on-background',backgroundcolor.get('lab.l') < 70 ? backgroundcolor.brighten(4) : backgroundcolor.darken(4));
    }
});






