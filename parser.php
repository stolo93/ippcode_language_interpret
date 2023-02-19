<?php
# Redirect error messages to stderr
ini_set('display_errors', 'stderr');

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
        error_log("Wrong or missing header in the input file. Header: ".$header);
        exit(21);
    }
}

function check_variable($var)
{
    #TODO implement
    return true;
}

function check_label($label)
{
    #TODO implement
    return true;
}

function check_symbol($symbol)
{
    #TODO implement
    return true;
}

function check_type($type)
{
    switch ($type) {
        case "int":
        case "bool":
        case "string":
            return true;
        default:
            error_log("Invalid type: ".$type."\n");
            exit (23);
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
            error_log("Invalid type in arg_get_value(): ".$arg."\n");
            exit(23);
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
        error_log("Help specified with another parameter\n");
        exit(10);
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
        error_log("Error with opening file: ".$options["source"]."\n");
        exit(11);
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
            check_variable($line[1]);
            add_instruction($xml, $inst_ord++, strtoupper($line[0]), $line[1]);
            break;

        # <symbol>
        case "PUSHS":
        case "WRITE":
        case "EXIT":
        case "DPRINT":
            check_argc($line, 2);
            check_symbol($line[1]);
            add_instruction($xml, $inst_ord++, strtoupper($line[0]), $line[1]);
            break;

        # <label>
        case "CALL":
        case "LABEL":
        case "JUMP":
            check_argc($line, 2);
            check_label($line[1]);
            add_instruction($xml, $inst_ord++, strtoupper($line[0]), $line[1]);
            break;

        # <var> <symbol>
        case "MOVE":
        case "INT2CHAR":
        case "STRLEN":
        case "TYPE":
        case "NOT":
            check_argc($line, 3);
            check_variable($line[1]);
            check_symbol($line[2]);
            add_instruction($xml, $inst_ord++, strtoupper($line[0]), $line[1], $line[2]);
            break;

        # <var> <type>
        case "READ":
            check_argc($line, 3);
            check_variable($line[1]);
            check_type($line[2]);
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
            check_variable($line[1]);
            check_symbol($line[2]);
            check_symbol($line[3]);
            add_instruction($xml, $inst_ord++, strtoupper($line[0]), $line[1], $line[2], $line[3]);
            break;

        # <label> <symb1> <symb2>
        case "JUMPIFEQ":
        case "JUMPIFNEQ":
            check_argc($line, 4);
            check_label($line[1]);
            check_symbol($line[2]);
            check_symbol($line[3]);
            add_instruction($xml, $inst_ord++, strtoupper($line[0]), $line[1], $line[2], $line[3]);
            break;

        default:
            error_log("Invalid instruction opcode: ".$line[0]."\n");
            exit(22);
    }
}

#Print formated XML to stdout
$dom = new DOMDocument("1.0");
$dom->formatOutput = true;
$dom->loadXML($xml->asXML());
echo $dom->saveXML();
?>