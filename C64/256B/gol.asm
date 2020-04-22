//Game of Life C64 - 256 bytes. By Ruk in 2012
//This implementation is actually only 252 bytes, not 256 as in the d64 on csdb (and youtube)
//Compile with KickAssembler. Enjoy

.pc =$0801 "Basic upstart"
   .text "RUK!"  
   .byte $9e  // sys
   .text toIntString(init)
   .byte 0,0,0

.pc = $080d "Begin"

init:
	sei
	jsr init_zp
	sty $0908
	sty $d016			
	sty $fe
	sty $fc
	lda #$d8			// set $d800 to lt blue
	sta $fd
	sta $d406
	ldx #252
!:	lda #$20
	sta ($f8),y
	sta ($fe),y
	lda #$FE
	sta $0909,y			// char $21 is set to a 7x7 pixel block
	sta ($fc),y
	iny
	bne !-
	inc $f9
	inc $ff
	inc $fd 
	inx
	bne !-
	dex
	stx $d418
nextblock:
	ldx #$08
	lda ($31),y	
shift:  
	asl $08ff,x			// blank char $20
	asl	
	bcc skip
sm:	inc $042a
skip:
	inc sm+1
	bne !+
	inc sm+2
!:	
	dex
	bne shift
	iny
    	cpy #$66
    	bne nextblock
	sty $d020			// darkblue border
	sty $d405
loop:
	jsr init_zp		
	clc									
screen:	
	ldy #0
row:								
	lda ($f8),y									   
	adc ($fa),y					
	adc ($fc),y								
	iny					
	iny
	adc ($f8),y		
	adc ($fa),y			
	adc ($fc),y		
	dey			
	adc ($f8),y		
	adc ($fc),y		
	tax
	lda ($fa),y			// e.g. $0429
	lsr				// a = $10
	bcs livecell
deadcell:	
	lsr		   	        // $08 table for deadcell
	.byte $21			// bit $0ca9
livecell:
	lda #$0c			// 00110000  	<- neighbour table
!:	lsr				// shift neighbour table
	dex 
	bpl !-
	lda #$10
	rol				//ROL in active/dead cell
	sta ($fe),y			//Store in buffer
	cmp ($fa),y
	beq !+				//no change
	inc $f7				//increase pitch
	bpl !+
	dec $f7				//clamp it
!:
	cpy #38				//skip 1st and last column
	bne row

	lda $fa						
	sta $f8
	lda $fb
	sta $f9
	
	lda $fc
	sta $fa
	sta $fe
	//clc				//carry i s set by cpy above
	adc #$27			//therefore, we add 27+c
	sta $fc
	tax
	lda $fd
	sta $fb
	eor #$20
	sta $ff
	bcc !+
	inc $fd
!:  	cpx #$e8			// it won't be e8 until we're done ;) 28+28+28...
	bne screen
	
	eor #$03			// AND should suffice. However, it is still 2 bytes
	sta init_zp + 1		
	//sec				// carry is set by cpx above
	rol
	asl				 
!:	bit $d011					
	bpl !-
	sta $d018			//switch screen
	lda $f7
	beq nosound
	ldx #$11
nosound:
	lsr
	sta $d401
	stx $d404
	bpl loop			
init_zp:
	lda #$04
	sta $f9
	sta $fb
	sta $fd
	eor #$20			// lda imm value above is modified in loop
	sta $ff
	lda #$28
	sta $fa
	sta $fe
	asl
	sta $fc
	ldy #0
	sty $f8
	sty $f7
	rts	
	
