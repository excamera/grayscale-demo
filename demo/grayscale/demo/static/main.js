var output_mpd = "http://dash.edgesuite.net/envivio/EnvivioDash3/manifest.mpd";

function main() {
	console.log("Inside main()");
	var s3url = document.getElementById('url');
	var exe_script = "/home/kvasukib/lambda/pipeline/external/mu/src/lambdaize/run.sh ${s3url}";
	var exec = require('child_process').exec, child;
	child = exec(${exe_script},
    			function (error, stdout, stderr) {
			        console.log('stdout: ' + stdout);
			        console.log('stderr: ' + stderr);
			        if (error !== null) {
			             console.log('exec error: ' + error);
        			}
    			});
	child();
}
