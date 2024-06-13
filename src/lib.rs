//! # Interpreter Tutorial
//! 
//! Something something, basic interpreter in rust. 


/// run a basic input loop where the user will be prompted with `@>` or `#>` to enter
/// code to be executed.
/// 
/// ---
/// 
/// it can be started with `interpreter::run()` or by running the interpreter executable.
/// 

// use tts;
use std::process::Command;

const PYTHON: &str = "C:\\Users\\abbyd\\AppData\\Local\\Programs\\Python\\Python312\\python.exe";


pub fn run() {

    let output = Command::new(PYTHON)
        // .env("PATH", "/bin")
        .args(["src/py/tts.py"])
        .output()
        .expect("failed to execute process");
    
    let out = String::from_utf8(output.stdout).expect("Our bytes should be valid utf8");
    println!("out: {out}");

    // say("Something silly");
    // say("Something else silly");
}

pub fn say(msg: &str) {

    let cmd = "python tts.py";

    let output = if cfg!(target_os = "windows") {
        Command::new("cmd")
            .args(["/C", cmd])
            .output()
            .expect("failed to execute process")
    } else {
        Command::new("sh")
            .arg("-c")
            .arg(cmd)
            .output()
            .expect("failed to execute process")
    };
    
    let out = output.stdout;
    println!("out: {out:?}");


    println!("Saying \"{msg}\"");
}
