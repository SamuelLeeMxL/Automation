package require tcom

set ::fp [open "abc.csv" a+]
close $::fp
set excel [::tcom::ref createobj Excel.Application]
$excel Visible 0

set workbooks [$excel Workbooks]
set workbook [$workbooks Open {C:\Python39\Scripts\AutoMation_1\abc.csv}]

set worksheets [$workbook Worksheets]
    
set sheet1 [$worksheets Item [expr 1]]

set cells1 [$sheet1 Cells]

set R [expr 1]
set C "A"
$cells1 Item $R $C "123"
#set R1C1 [[$cells1 Item $R $C] 123]
$workbook Save
$excel Quit