/* workaround safari issues */

var isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);

function updateContext(opts) {
    // Safari 11 or newer automatically suspends new AudioContext's that aren't
    // created in response to a user-gesture, like a click or tap, so create one
    // here (inc. the script processor)
    var AudioContext = window.AudioContext || window.webkitAudioContext;
    var context = new AudioContext();
    var processor = context.createScriptProcessor(1024, 1, 1);

    opts.plugins.wavesurfer.audioContext = context;
    opts.plugins.wavesurfer.audioScriptProcessor = processor;
}