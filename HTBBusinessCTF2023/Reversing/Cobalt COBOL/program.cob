IDENTIFICATION DIVISION.
    PROGRAM-ID. CC.


DATA DIVISION.
    WORKING-STORAGE SECTION.
        01 F.
            05 R OCCURS 9 TIMES.
                10 FC OCCURS 9 TIMES.
                    15 C PIC 9(1).

        01 A.
            05 AF OCCURS 9 TIMES INDEXED BY FIN.
                10 AFF PIC 9(1).

        01 T PIC 9(1).
        01 I PIC 9(3).
        01 P PIC X(1548) VALUE
            "K36_B}8963AC 7EHC_IMGDMRKHQWOLU}SPY4WT09{X552}9 63BD 7FIC_JNG"&
            "DNSKHRXOLV0SPZ5WT21{X662} _63CE 7GJC_KOGDOTKHSYOLW1SP}ZWT32{X"&
            "772}_A63DF 7HKC_LPGDPUKHTZOLYVSP0{WT43{X882}AB63EG 7ILC_MQGDQ"&
            "VKHVROLZWSP1}WT54{X992}BC63FH 7JMC_NRGDSNKHWSOL{XSP20WT65{X  "&
            "2}CD63GI 7KNC_PJGDTOKHXTOL}YSP31WT76{X__2}DE63HJ 7MFC_QKGDUPK"&
            "HYUOL0ZSP42WT87{XAA2}EF6SL5CDP9GITBKNXFOS}JSX3NW07R{5_V2 DZ6D"&
            "HKRK4CCO8GHSAKMWEOR{ISW2MW}6Q{4 U29CY6CGJQJ3CBN7GGR_KLVDOQZHS"&
            "V1LW{5P{39T28BX6BFIPI2CAM6GFQ KKUCOPYGSU0KWZ4O{28S27AW6AEHOH1"&
            "C_L5GEP9KJTBOOXFST}JWY3N{17R26_V6_DGNG0C K4GDO8KISAONWESS{IWX"&
            "2M{06Q25 U6 CFMF}C9J3GCN7KHR_OMVDSRZHWW1L{}5P249T69BELE{C8I2G"&
            "BM6KGQ OLUCSQYGWV0K{{4O238S68ADKDZC7H1GAL5KFP9OKTBSPXFWU}J{Z3"&
            "N227R67_CJCY56G0  K4DCO8IGSANKWESO{IXS2M0W6Q5{ BIBX46F}9 J3CC"&
            "N7HGR_MKVDROZHWS1L}W5P4{9AHAW36E{8 I2BCM6GGQ LKUCQOYGVS0K{W4O"&
            "3{8_G_V26DZ7 H1ACL5FGP9KKTBPOXFUS}JZW3N2{7 F U16CY6 G0_CK4EGO"&
            "8JKSAOOWETS{IYW2M1{69E9T06BX5 F} CJ3DGN7IKR_NOVDSSZHXW1L0{58D"&
            "8S}6AW4 E{9CI2CGM6HKQ MOUCRSYGWW0K}{47C7R{6_V3 DZ8CH1BGL5GKP9"&
            "LOTBQSXFVW}J{{36B6QZ6 U2 CY7CG0AGK4FKO8KOSAPSWEUW{IZ{25A5PYZ9"&
            "T02BX47F}99J3BCN7FHR_KJVDOOZHST14_4OX}8S}4AW39E{8_I2AEM6EJQ J"&
            "LUCNQYGRV03 3NW17R{6_V2_DZ7BH1_GL5DLP9INTBMSXFQX}292MYW6Q0} U"&
            "44CY96G0B_K4FEO8KGSAOLWESQ{181LXY5P}19T36BX88F}ABJ3EGN7JIR_NN"&
            "VDRSZ070KW{4O{38S28AW7 E{_DI2DIM6IKQ MPUCQUY}6}JYT3N0Y7R41_V9"&
            "3DZB8H1FBL5KDP9OITBSNX{5{IXV2M}{6Q33 U85CYA G0EDK4JFO8NKSARPW"&
            "Z4ZHWX1L{05P259T77BX_AF}DFJ3IHN7MMR_QRVYAGOPTVY}WW}2R{Z4}292 "&
            "850  EGDBHCIN_KNRJPPMOOSKWSUXV140}{V657 5867FD4GFDCLEGPKPDSUM"&
            "TRRXWSXO21{ZZ3}692}AB28 5CE8JG_GNCNKFPSIOTLZTOZ1R0}U05X9 {A91"&
            "AB4AC7HE HNBJJEQQGMNOV}".

        01 PB PIC X(11).
        01 P0 PIC 9(8) VALUE 1.
        
        01 P1 OCCURS 9 TIMES.
            05 Q PIC 9(4) VALUE 0.
        
        01 PS PIC 9(1) VALUE 0.
        
        01 PRS OCCURS 9 TIMES.
            05 PR PIC 9(1).
        
        01 PWK.
            05 PK OCCURS 20 TIMES.
                10 PKF PIC 9(1) VALUE 0.

        01 PKI PIC 9(2) VALUE 1.
        01 R0 PIC 9(24).
        01 R1 PIC 9(20).
        01 RI PIC 9(2).
        01 RC PIC X(1).
        01 FI PIC 9(2).
        01 RCS PIC X(40) VALUE " _ABCDEFGHIJKLMNOPQRSTUVWXYZ{}0123456789".
        
        01 FW.
            05 FL OCCURS 30 TIMES.
                10 FC PIC X(1).


PROCEDURE DIVISION.
    INITIALIZE T
    INITIALIZE F

    PERFORM VM WITH TEST AFTER UNTIL PS EQUALS 1
    IF T IS ZERO THEN
        PERFORM DECODE
    ELSE
        DISPLAY
            "WRONG"
        END-DISPLAY
    END-IF
    STOP RUN.

    CONV.
        MOVE 5 TO RI
        PERFORM 10 TIMES
            COMPUTE
                R1 = FUNCTION MOD (R0(RI:2) 40) + 1
            END-COMPUTE
            MOVE RCS(R1:1) TO RC
            MOVE RCS(R1:1) TO FL(FI)
            ADD 2 TO RI
            ADD 1 TO FI
        END-PERFORM.

    DECODE.
        MOVE 1 TO FI
        MOVE PWK TO R0(5:20)
        COMPUTE
            R0 = FUNCTION MOD (((519*R0) - 9524936758751936028873) 18446744073709551557)
        END-COMPUTE
        PERFORM CONV
        MOVE PWK TO R0(5:20)
        COMPUTE
            R0 = FUNCTION MOD (((655*R0) - 5139944510939323535175) 18446744073709551557)
        END-COMPUTE
        PERFORM CONV
        MOVE PWK TO R0(5:20)
        COMPUTE
            R0 = FUNCTION MOD(((301*R0) - 5165552119864536862147) 18446744073709551557)      
        END-COMPUTE
        PERFORM CONV
        DISPLAY FW.
    
    VM.
        MOVE P(P0:11) TO PB
        INITIALIZE Q(1)
        PERFORM 11 TIMES
            ADD 1 TO Q(1)
            INITIALIZE RI
            INSPECT RCS TALLYING RI FOR CHARACTERS BEFORE INITIAL PB(Q(1):1)
            COMPUTE
                RI = FUNCTION MOD ((RI - P0 - Q(1) + 1) 40)
            END-COMPUTE
            ADD 1 TO RI
            MOVE RCS(RI:1) TO PB(Q(1):1)
        END-PERFORM

        EVALUATE PB(1:1)
            WHEN "W"
                MOVE PB(2:1) TO Q(1)
                MOVE PB(3:9) TO R(Q(1))
                ADD 11 TO P0
            WHEN "J"
                MOVE PB(2:4) TO Q(1)
                ADD 5 TO P0
                ADD Q(1) TO P0
            WHEN "R"
                MOVE Q(9) TO P0
            WHEN "X"
                MOVE PB(2:4) TO Q(1)
                ADD 5 TO P0
                MOVE P0 TO Q(9)
                MOVE Q(1) TO P0
            WHEN "I"
                EVALUATE PB(2:1)
                    WHEN NUMERIC
                        MOVE PB(2:1) TO Q(1)
                        INITIALIZE PR(Q(1))
                    WHEN "A"
                        INITIALIZE A
                END-EVALUATE
                ADD 2 TO P0
            WHEN "V"
                MOVE PB(2:1) TO Q(1)
                MOVE PB(3:1) TO Q(2)
                ADD 3 TO P0
                MOVE C(Q(2), Q(1)) TO PR(1)
            WHEN "Y"
                MOVE PB(2:1) TO Q(1)
                MOVE PB(3:1) TO Q(2)
                ADD 3 TO P0  
                ACCEPT
                    PR(1)
                END-ACCEPT
                MOVE PR(1) TO PK(PKI)
                ADD 1 TO PKI
                MOVE PR(1) TO C(Q(2), Q(1))
            WHEN "Z"
                ADD 1 TO P0
                IF PR(1) IS EQUAL TO ZERO THEN
                    MOVE 1 TO T
                END-IF
            WHEN "A"
                ADD 1 TO P0
                MOVE 1 TO AFF(PR(1))
            WHEN "C"
                ADD 1 TO P0
                INITIALIZE FIN
                SEARCH AF
                    WHEN AF(FIN) = ZERO
                        MOVE 1 TO T
                END-SEARCH
            WHEN "_"
                MOVE 1 TO PS
            WHEN OTHER
                DISPLAY "?"
        END-EVALUATE.
