<?php
# Redirect error messages to stderr
ini_set('display_errors', 'stderr');

function error($msg, $exit_code){
    error_log($msg."\n");
    exit(intval($exit_code));
}

function is_arg($name, $options_array)
{
    if(array_key_exists($name, $options_array) || array_key_exists($name[0], $options_array)){
        return true;
    }
    else{
        return false;
    }
}

function remove_comment(&$string, $com_symbol)
{
    $pos = strpos($string, $com_symbol);
    if ( $pos === false ){
        return;
    }
    $string = substr($string,0, $pos);
}

function check_header($header)
{
    if ( ! ($header === ".IPPcode23") ){
        error("Wrong or missing header in the input file. Header: ".$header, 21);
    }
}

function check_variable($var)
{
    $pos_delim = strpos($var, "@");
    if ( $pos_delim == false ) { #== because @ can not be at index 0 (GF@...)
        return false;
    }

    $frame = substr($var, 0, $pos_delim);
    if ( ! preg_match("/^((gf)|(lf)|(tf))$/i", $frame) ){
        return false;
    }

    $var_id = substr($var, $pos_delim+1);
    if ( !preg_match("/^[ _, -, $, &, %, *, !, ?, a-z,A-Z][a-z,A-Z,0-9]*$/",$var_id)){
        return false;
    }

    return true;
}

function check_label($label)
{
    if ( !preg_match("/^[ _, -, $, &, %, *, !, ?, a-z,A-Z][a-z,A-Z,0-9]*$/",$label)){
        return false;
    }
    else{
        return true;
    }
}

function check_symbol($symbol)
{
    # symbol may be a variable
    if (check_variable($symbol)){
        return true;
    }

    $pos_delim = strpos($symbol, "@");
    if ( ! $pos_delim){
        return false;
    }

    $type = substr($symbol, 0, $pos_delim);
    $value = substr($symbol, $pos_delim+1);

    switch ($type) {
        case "int":
            if ( preg_match("/^(([1-9][0-9]*(_[0-9]+)*|0)|(0[xX][0-9a-fA-F]+(_[0-9a-fA-F]+)*)|(0[oO]?[0-7]+(_[0-7]+)*)|(0[bB][01]+(_[01]+)*))$/", $value)){
                return true;
            }
            break;

        case "bool":
            if (preg_match("/^((true)|(false))$/i", $value)){
                return true;
            }
            break;

        case "string":
            return true;

        case "nil":
            if ( $value == "nil"){
                return true;
            }
            break;

        default:
            return false;
    }

    return false;
}

function check_type($type)
{
    switch ($type) {
        case "int":
        case "bool":
        case "string":
            return true;
        default:
            return false;
    }
}

function check_argc($line, $count)
{
    if (count($line) != $count){
        error_log("Invalid number of arguments for operation: ".$line[0]."\n");
        exit(23);
    }
}

function replace_special_in_string($string)
{
    # < = &lt
    # > = &gt
    # & = &amp
    # ...
    return str_replace(array("<", ">","&"), array("&lt", "&gt", "&amp"), $string);
}

function arg_get_type($arg)
{
    #Domain = {int, bool, string, nil, label, type, var}
    $pos_delim = strpos($arg, "@");
    if ( $pos_delim === false ) { # No @ found means label or type

        # Type
        if ( $arg == "int" || $arg == "string" || $arg == "bool"){
            return "type";
        }

        # Label
        else{
            return "label";
        }
    }

    $type = substr($arg, 0, $pos_delim);
    # May be a variable
    if (strtoupper($type) == "LF" || strtoupper($type) == "GF" || strtoupper($type) == "TF"){
        return "var";
    }

    return $type;
}

function arg_get_value($arg)
{
    #for strings use replace_special_in_string()
    # wo/ type and @
    # w/ uppercase frame and @

    $pos_delim = strpos($arg, "@");

    if ( $pos_delim === false ){ # No "@" found means label or type
        return $arg;
    }

    $type = substr($arg, 0, $pos_delim);
    switch (strtoupper($type)) {
        case "INT":
        case "BOOL":
        case "NIL":
            return substr($arg, $pos_delim + 1);

        case "STRING":
            return replace_special_in_string(substr($arg, $pos_delim+1));

        case "GF":
        case "LF":
        case "TF":
            return strtoupper($type).substr($arg, $pos_delim); #uppercase(FRAME) + @ + var_id

        default:
            error("Invalid type in arg_get_value(): ".$arg, 23);
        }
}

function add_arg($instruction, $order, $arg)
{
    $new_arg = $instruction->addChild(("arg".$order), arg_get_value($arg));
    $new_arg->addAttribute("type", arg_get_type($arg));
}
function add_instruction($xml, $order, $opcode, $arg1=null, $arg2=null, $arg3=null)
{
    $new_instruction = $xml->addChild("instruction");
    $new_instruction->addAttribute("order", $order);
    $new_instruction->addAttribute("opcode", strtoupper($opcode));

    if ($arg1 != null){
        add_arg($new_instruction, 1, $arg1);
    }

    if ($arg2 != null){
        add_arg($new_instruction, 2, $arg2);
    }

    if ($arg3 != null){
        add_arg($new_instruction, 3, $arg3);
    }

}

########################################################
########################################################
########### PROGRAM ENTRY POINT ########################

#TODO write propper help message
$help = "HELP";

# Parse program parameters
$opts_short = 'hs:';
$opts_long = array(
    "source:",
    "help"
);

$options = getopt($opts_short, $opts_long);

# Check for --help or -h
if ( is_arg("help", $options) ){
    if ( is_arg("source", $options) ){
        error("Help specified with another parameter", 10);
    }
    else{
        echo($help);
        exit(0);
    }
}

# Get input file
$file_input;
if ( is_arg("source", $options)){
    $file_input = fopen($options["source"],"r");
    if ($file_input == false){
        error("Error with opening file: ".$options["source"], 11);
    }
}
else{
    $file_input = STDIN;
}

# Create an xml which will contain the program
$xml = new SimpleXMLElement("<?xml version=\"1.0\" encoding=\"UTF-8\"?><program></program>");
$xml->addAttribute("language", "IPPcode23");

$instructions = array();
$inst_ord = 1;
$header_checked = false;

while ($line = fgets($file_input)){
    # Remove comments and skip empty lines
    remove_comment($line, "#");
    if ( trim($line) == ""){
        continue;
    }

    $line = explode(" ", trim($line));

    if (! $header_checked ){
        check_header($line[0]);
        $header_checked = true;
        continue;
    }

    switch (strtoupper($line[0])) {
        # no arguments
        case "CREATEFRAME":
        case "PUSHFRAME":
        case "POPFRAME":
        case "RETURN":
        case "BREAK":
            check_argc($line, 1); #one more for opcode
            add_instruction($xml, $inst_ord++, strtoupper($line[0]));
            break;

        # <var>
        case "DEFVAR":
        case "POPS":
            check_argc($line, 2);
            if (! check_variable($line[1]) ){
                error("Invalid argument - variable: ".$line[1], 23);
            }
            add_instruction($xml, $inst_ord++, strtoupper($line[0]), $line[1]);
            break;

        # <symbol>
        case "PUSHS":
        case "WRITE":
        case "EXIT":
        case "DPRINT":
            check_argc($line, 2);
            if ( ! check_symbol($line[1])){
                error("Invalid argument - symbol: ".$line[1], 23);
            }
            add_instruction($xml, $inst_ord++, strtoupper($line[0]), $line[1]);
            break;

        # <label>
        case "CALL":
        case "LABEL":
        case "JUMP":
            check_argc($line, 2);
            if ( !check_label($line[1])){
                error("Invalid argument - label: ".$line[1], 23);
            }
            add_instruction($xml, $inst_ord++, strtoupper($line[0]), $line[1]);
            break;

        # <var> <symbol>
        case "MOVE":
        case "INT2CHAR":
        case "STRLEN":
        case "TYPE":
        case "NOT":
            check_argc($line, 3);
            if ( ! (check_variable($line[1]) && check_symbol($line[2])) ){
                error("Invalid arguments - variable, symbol: ".$line[1]." ".$line[2], 23);
            }
            add_instruction($xml, $inst_ord++, strtoupper($line[0]), $line[1], $line[2]);
            break;

        # <var> <type>
        case "READ":
            check_argc($line, 3);
            if (! (check_variable($line[1]) && check_type($line[2]))){
                error("Invalid arguments - variable, type: ".$line[1]." ".$line[2], 23);
            }
            add_instruction($xml, $inst_ord++, strtoupper($line[0]), $line[1], $line[2]);
            break;

        # <var> <symb1> <symb2>
        case "ADD":
        case "SUB":
        case "MUL":
        case "IDIV":
        case "LT":
        case "GT":
        case "EQ":
        case "AND":
        case "OR":
        case "STRI2INT":
        case "CONCAT":
        case "GETCHAR":
        case "SETCHAR":
            check_argc($line, 4);
            if (! (check_variable($line[1]) && check_symbol($line[2]) && check_symbol($line[3]))){
                error("Invalid arguments - variable, symbol, symbol: ".$line[1]." ".$line[2]." ".$line[3], 23);
            }
            add_instruction($xml, $inst_ord++, strtoupper($line[0]), $line[1], $line[2], $line[3]);
            break;

        # <label> <symb1> <symb2>
        case "JUMPIFEQ":
        case "JUMPIFNEQ":
            check_argc($line, 4);
            if ( ! (check_label($line[1]) && check_symbol($line[2]) && check_symbol($line[3]))){
                error("Invalid arguments - label, symbol, symbol :".$line[1]." ".$line[2]." ".$line[3], 23);
            }
            add_instruction($xml, $inst_ord++, strtoupper($line[0]), $line[1], $line[2], $line[3]);
            break;

        default:
            error("Invalid instruction opcode: ".$line[0], 22);
    }
}

#Print formated XML to stdout
$dom = new DOMDocument("1.0");
$dom->formatOutput = true;
$dom->loadXML($xml->asXML());
echo $dom->saveXML();
?>