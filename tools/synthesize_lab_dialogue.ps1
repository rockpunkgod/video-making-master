param([Parameter(Mandatory=$true)][string]$OutputPath,[Parameter(Mandatory=$true)][string]$Text)
Add-Type -AssemblyName System.Speech
$speech=New-Object System.Speech.Synthesis.SpeechSynthesizer
try{
 $speech.SelectVoice('Microsoft Zira Desktop');$speech.Rate=-1
 $format=New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo (48000),([System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen),([System.Speech.AudioFormat.AudioChannel]::Stereo)
 $speech.SetOutputToWaveFile($OutputPath,$format);$speech.Speak($Text)
}finally{$speech.Dispose()}

