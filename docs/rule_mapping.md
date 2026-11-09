# SDTM Rule Mapping

This table maps each CORE rule in [`sdtm_rules/`](../sdtm_rules) to the CDISC and FDA rule IDs it implements,
as listed under `Authorities` in the rule's YAML.

- **CDISC ID(s)**: `CG####` = SDTM/SDTMIG Conformance Rules, `SEND##` = SEND Conformance Rules, `TIG####` = TIG Conformance Rules
- **FDA ID(s)**: `FB####` / `TRC####` = FDA Business Rules
- **Executability**: the `Executability` value in the rule's YAML
- **Implementation Notes**: implementation details for the rule (e.g. why it may over- or underreport, or how a CDISC/FDA rule was split across CORE rules), where available

There are 629 CORE rules: 485 cite a CDISC rule, 192 cite an FDA rule, and 48 cite both.
CORE-000249
> This file is a snapshot of the rule YAMLs. If you add a rule or change its `Authorities` or `Executability`, update this file too.

## CORE → CDISC / FDA

| CORE ID | Status | Executability | CDISC ID(s) | FDA ID(s) | Implementation Notes |
| --- | --- | --- | --- | --- | --- |
| [CORE-000001](../sdtm_rules/CORE-000001) | Published | Fully Executable | CG0176, TIG0405 | — | — |
| [CORE-000002](../sdtm_rules/CORE-000002) | Published | Fully Executable | CG0208 | — | — |
| [CORE-000003](../sdtm_rules/CORE-000003) | Published | Fully Executable | CG0299 | — | — |
| [CORE-000004](../sdtm_rules/CORE-000004) | Published | Fully Executable | CG0101, TIG0366 | — | — |
| [CORE-000005](../sdtm_rules/CORE-000005) | Published | Fully Executable | CG0102 | — | — |
| [CORE-000006](../sdtm_rules/CORE-000006) | Published | Fully Executable | CG0131, TIG0381 | — | — |
| [CORE-000007](../sdtm_rules/CORE-000007) | Published | Fully Executable | CG0435, TIG0587 | FB0606 | — |
| [CORE-000008](../sdtm_rules/CORE-000008) | Published | Fully Executable | CG0132 | FB0601 | — |
| [CORE-000009](../sdtm_rules/CORE-000009) | Published | Fully Executable | CG0152, SEND124.1, TIG0061, TIG0393 | — | — |
| [CORE-000010](../sdtm_rules/CORE-000010) | Published | Fully Executable | CG0153, TIG0394 | — | — |
| [CORE-000011](../sdtm_rules/CORE-000011) | Published | Fully Executable | CG0175, TIG0404 | — | — |
| [CORE-000012](../sdtm_rules/CORE-000012) | Published | Fully Executable | CG0040, TIG0319 | — | — |
| [CORE-000013](../sdtm_rules/CORE-000013) | Published | Fully Executable | CG0044, TIG0323 | — | — |
| [CORE-000014](../sdtm_rules/CORE-000014) | Published | Fully Executable | CG0087, TIG0352 | — | — |
| [CORE-000015](../sdtm_rules/CORE-000015) | Published | Fully Executable | CG0088, TIG0353 | — | — |
| [CORE-000016](../sdtm_rules/CORE-000016) | Published | Fully Executable | CG0089, TIG0354 | — | — |
| [CORE-000017](../sdtm_rules/CORE-000017) | Published | Fully Executable | CG0166, TIG0398 | — | — |
| [CORE-000018](../sdtm_rules/CORE-000018) | Published | Fully Executable | CG0086, TIG0351 | — | — |
| [CORE-000019](../sdtm_rules/CORE-000019) | Published | Fully Executable | CG0311, SEND3, TIG0211, TIG0486 | — | — |
| [CORE-000020](../sdtm_rules/CORE-000020) | Published | Fully Executable | CG0206, TIG0426 | — | — |
| [CORE-000021](../sdtm_rules/CORE-000021) | Published | Fully Executable | CG0397, TIG0559 | — | — |
| [CORE-000022](../sdtm_rules/CORE-000022) | Published | Fully Executable | CG0041, TIG0320 | — | — |
| [CORE-000023](../sdtm_rules/CORE-000023) | Published | Fully Executable | CG0084, TIG0349 | — | — |
| [CORE-000024](../sdtm_rules/CORE-000024) | Published | Fully Executable | CG0082, TIG0347 | — | — |
| [CORE-000025](../sdtm_rules/CORE-000025) | Published | Fully Executable | CG0177, TIG0406 | — | — |
| [CORE-000026](../sdtm_rules/CORE-000026) | Published | Fully Executable | CG0468, TIG0598 | — | — |
| [CORE-000027](../sdtm_rules/CORE-000027) | Published | Fully Executable | CG0328, CG0329, SEND214, TIG0141, TIG0496, TIG0497 | — | — |
| [CORE-000028](../sdtm_rules/CORE-000028) | Published | Fully Executable | CG0008, TIG0293 | — | — |
| [CORE-000029](../sdtm_rules/CORE-000029) | Published | Fully Executable | CG0661, TIG0697 | — | — |
| [CORE-000030](../sdtm_rules/CORE-000030) | Published | Fully Executable | CG0053, TIG0329 | — | — |
| [CORE-000031](../sdtm_rules/CORE-000031) | Published | Fully Executable | CG0659 | — | Note: Rule is split up in 3 rules.<br>- CORE-000031 for QS and FT - Raise an error when --EVAL is present in the QS or FT dataset.<br>- CORE-002124: For RS domain when all RSCAT records in the RS domain have values from the CCCAT code list (Clinical Classification Use case) - Raise an error when RSCAT is only populated with values from the Clinical Classification Use Case as per the define.xml document, but RSEVAL is present in the RS dataset.<br>- CORE-002126: For RS domain some RSCAT records in the RS domain have values from the CCCAT code list (Clinical Classification Use case) but also other codelists are used like for example ONCRSCAT. - Raise an error when some records in the RS dataset have RSCAT populated with values from the Clinical Classification Use Case as per the define.xml document but RSEVAL for those RSCAT records is populated.<br>For the RS domain implementation of the rule some assumptions where made: In case only 1 codelist is used, the codelist will be defined at variable level.In case more than one codelist is used to populate RSCAT, the codelist will be defined at value level. |
| [CORE-000032](../sdtm_rules/CORE-000032) | Published | Fully Executable | CG0660 | — | Note: Rule is split up in 3 rules.<br>- CORE-000032 for QS and FT - Raise an error when --EVALID is present in the QS or FT dataset.<br>- CORE-002125: For RS domain when all RSCAT records in the RS domain have values from the CCCAT code list (Clinical Classification Use case) - Raise an error when RSCAT is only populated with values from the Clinical Classification Use Case as per the define.xml document, but RSEVALID is present in the RS dataset.<br>- CORE-002127: For RS domain some RSCAT records in the RS domain have values from the CCCAT code list (Clinical Classification Use case) but also other codelists are used like for example ONCRSCAT. - Raise an error when some records in the RS dataset have RSCAT populated with values from the Clinical Classification Use Case as per the define.xml document but RSEVALID for those RSCAT records is populated.<br>For the RS domain implementation of the rule some assumptions where made: In case only 1 codelist is used, the codelist will be defined at variable level.In case more than one codelist is used to populate RSCAT, the codelist will be defined at value level. |
| [CORE-000033](../sdtm_rules/CORE-000033) | Published | Fully Executable | CG0065, TIG0337 | — | — |
| [CORE-000034](../sdtm_rules/CORE-000034) | Published | Fully Executable | CG0069, TIG0339 | — | — |
| [CORE-000035](../sdtm_rules/CORE-000035) | Published | Fully Executable | CG0658, TIG0696 | — | — |
| [CORE-000036](../sdtm_rules/CORE-000036) | Published | Fully Executable | CG0657, TIG0695 | — | — |
| [CORE-000037](../sdtm_rules/CORE-000037) | Published | Fully Executable | CG0653, TIG0691 | — | — |
| [CORE-000038](../sdtm_rules/CORE-000038) | Published | Fully Executable | CG0654, TIG0692 | — | — |
| [CORE-000039](../sdtm_rules/CORE-000039) | Published | Fully Executable | CG0655, TIG0693 | — | — |
| [CORE-000040](../sdtm_rules/CORE-000040) | Published | Fully Executable | CG0656, TIG0694 | — | — |
| [CORE-000041](../sdtm_rules/CORE-000041) | Published | Partially Executable - Possible Underreporting | CG0459, CG0649, TIG0689 | — | Explanation: Rule is programmatically only checking for ISO 21090 null flavor values in TSVAL and not for synonyms. Cases where synonyms for null flavors are used in TSVAL and TSVALNF not populated will not be detected by this rule. |
| [CORE-000042](../sdtm_rules/CORE-000042) | Published | Fully Executable | CG0647, TIG0687 | — | Note: This rule is checking whether a dataset not allowed for clinical trials is present in the data package. In case this dataset is not present, then the rule will skip because the requirement for the rule (the disallowed dataset) is not present. This is correct behaviour of the rule and the engine. Skip means, that your data pacakge is compliant with the conformance rule. |
| [CORE-000043](../sdtm_rules/CORE-000043) | Published | Fully Executable | CG0648, TIG0688 | — | Note: This rule is checking whether a dataset not allowed for clinical trials is present in the data package. In case this dataset is not present, then the rule will skip because the requirement for the rule (the disallowed dataset) is not present. This is correct behaviour of the rule and the engine. Skip means, that your data pacakge is compliant with the conformance rule. |
| [CORE-000044](../sdtm_rules/CORE-000044) | Published | Fully Executable | CG0646, TIG0686 | — | Note: This rule is checking whether a dataset not allowed for clinical trials is present in the data package. In case this dataset is not present, then the rule will skip because the requirement for the rule (the disallowed dataset) is not present. This is correct behaviour of the rule and the engine. Skip means, that your data pacakge is compliant with the conformance rule. |
| [CORE-000045](../sdtm_rules/CORE-000045) | Published | Fully Executable | CG0517, TIG0612 | — | — |
| [CORE-000046](../sdtm_rules/CORE-000046) | Published | Fully Executable | CG0519, TIG0614 | — | — |
| [CORE-000047](../sdtm_rules/CORE-000047) | Published | Partially Executable - Possible Overreporting | CG0518, TIG0613 | — | Explanation: The following part of the rule condition is not executable "Study does not use multi-stage arm assignments" and therefore cannot be included in the rule logic. As such the rule will also generate output for studies using multi-stage arm assignments. |
| [CORE-000048](../sdtm_rules/CORE-000048) | Published | Fully Executable | CG0621, TIG0662 | — | — |
| [CORE-000049](../sdtm_rules/CORE-000049) | Published | Fully Executable | CG0507, CG0622, TIG0602, TIG0663 | — | — |
| [CORE-000050](../sdtm_rules/CORE-000050) | Published | Fully Executable | CG0623, TIG0664 | — | — |
| [CORE-000051](../sdtm_rules/CORE-000051) | Published | Fully Executable | CG0624, TIG0665 | — | — |
| [CORE-000052](../sdtm_rules/CORE-000052) | Published | Fully Executable | CG0625, TIG0666 | — | — |
| [CORE-000054](../sdtm_rules/CORE-000054) | Published | Fully Executable | CG0627, TIG0668 | — | — |
| [CORE-000055](../sdtm_rules/CORE-000055) | Published | Fully Executable | CG0628, TIG0669 | — | — |
| [CORE-000056](../sdtm_rules/CORE-000056) | Published | Fully Executable | CG0629, TIG0670 | — | — |
| [CORE-000057](../sdtm_rules/CORE-000057) | Published | Fully Executable | CG0509, CG0630, TIG0604, TIG0671 | — | — |
| [CORE-000058](../sdtm_rules/CORE-000058) | Published | Fully Executable | CG0631, TIG0672 | — | — |
| [CORE-000059](../sdtm_rules/CORE-000059) | Published | Fully Executable | CG0632, TIG0673 | — | — |
| [CORE-000060](../sdtm_rules/CORE-000060) | Published | Fully Executable | CG0633, TIG0674 | — | — |
| [CORE-000061](../sdtm_rules/CORE-000061) | Published | Fully Executable | CG0634, TIG0675 | — | — |
| [CORE-000064](../sdtm_rules/CORE-000064) | Published | Fully Executable | CG0637, TIG0678 | — | — |
| [CORE-000065](../sdtm_rules/CORE-000065) | Published | Fully Executable | CG0638, TIG0679 | — | — |
| [CORE-000066](../sdtm_rules/CORE-000066) | Published | Fully Executable | CG0639, TIG0680 | — | — |
| [CORE-000067](../sdtm_rules/CORE-000067) | Published | Fully Executable | CG0640, TIG0681 | — | — |
| [CORE-000068](../sdtm_rules/CORE-000068) | Published | Fully Executable | CG0641, TIG0682 | — | — |
| [CORE-000069](../sdtm_rules/CORE-000069) | Published | Fully Executable | CG0642, TIG0683 | — | — |
| [CORE-000070](../sdtm_rules/CORE-000070) | Published | Fully Executable | CG0643, TIG0684 | — | — |
| [CORE-000071](../sdtm_rules/CORE-000071) | Published | Fully Executable | CG0644, TIG0685 | — | — |
| [CORE-000072](../sdtm_rules/CORE-000072) | Published | Fully Executable | CG0542 | — | — |
| [CORE-000073](../sdtm_rules/CORE-000073) | Published | Fully Executable | CG0533 | — | — |
| [CORE-000074](../sdtm_rules/CORE-000074) | Published | Fully Executable | CG0508, TIG0603 | — | — |
| [CORE-000075](../sdtm_rules/CORE-000075) | Published | Fully Executable | CG0304, TIG0481 | — | — |
| [CORE-000076](../sdtm_rules/CORE-000076) | Published | Fully Executable | CG0302 | — | — |
| [CORE-000077](../sdtm_rules/CORE-000077) | Published | Fully Executable | CG0301 | — | — |
| [CORE-000078](../sdtm_rules/CORE-000078) | Published | Fully Executable | CG0300 | — | — |
| [CORE-000079](../sdtm_rules/CORE-000079) | Published | Fully Executable | CG0095 | — | — |
| [CORE-000080](../sdtm_rules/CORE-000080) | Published | Fully Executable | CG0093, TIG0358 | — | — |
| [CORE-000081](../sdtm_rules/CORE-000081) | Published | Fully Executable | CG0056, TIG0330 | — | — |
| [CORE-000082](../sdtm_rules/CORE-000082) | Published | Fully Executable | CG0561 | — | — |
| [CORE-000083](../sdtm_rules/CORE-000083) | Published | Fully Executable | CG0553, TIG0641 | — | — |
| [CORE-000084](../sdtm_rules/CORE-000084) | Published | Fully Executable | CG0057, TIG0331 | — | — |
| [CORE-000085](../sdtm_rules/CORE-000085) | Published | Fully Executable | CG0059, TIG0333 | — | — |
| [CORE-000086](../sdtm_rules/CORE-000086) | Published | Fully Executable | CG0075, TIG0341 | — | — |
| [CORE-000087](../sdtm_rules/CORE-000087) | Published | Fully Executable | CG0387, TIG0549 | — | — |
| [CORE-000088](../sdtm_rules/CORE-000088) | Published | Fully Executable | CG0149, SEND25, TIG0169, TIG0390 | — | — |
| [CORE-000089](../sdtm_rules/CORE-000089) | Published | Fully Executable | CG0106 | — | — |
| [CORE-000090](../sdtm_rules/CORE-000090) | Published | Fully Executable | CG0164, TIG0397 | — | — |
| [CORE-000091](../sdtm_rules/CORE-000091) | Published | Fully Executable | CG0108 | — | — |
| [CORE-000092](../sdtm_rules/CORE-000092) | Published | Fully Executable | CG0110, CG0111, TIG0374, TIG0375 | — | — |
| [CORE-000093](../sdtm_rules/CORE-000093) | Published | Fully Executable | CG0114, TIG0377 | — | — |
| [CORE-000094](../sdtm_rules/CORE-000094) | Published | Fully Executable | CG0112, TIG0376 | — | — |
| [CORE-000095](../sdtm_rules/CORE-000095) | Published | Fully Executable | CG0211, TIG0430 | — | — |
| [CORE-000096](../sdtm_rules/CORE-000096) | Published | Fully Executable | CG0115, TIG0378 | — | — |
| [CORE-000097](../sdtm_rules/CORE-000097) | Published | Partially Executable - Possible Overreporting | CG0218, TIG0432 | — | Explanation: When SVSTDTC falls right on a tie between 2 EPOCHs, then it will validate the EPOCH of SV against both EPOCHs in SE. This will result in output that needs to be explained based on tie breakers defined on trial level. |
| [CORE-000098](../sdtm_rules/CORE-000098) | Published | Fully Executable | CG0116, TIG0379 | — | — |
| [CORE-000099](../sdtm_rules/CORE-000099) | Published | Fully Executable | CG0422, TIG0577 | — | — |
| [CORE-000100](../sdtm_rules/CORE-000100) | Published | Fully Executable | CG0423, TIG0578 | — | — |
| [CORE-000101](../sdtm_rules/CORE-000101) | Published | Fully Executable | CG0427, TIG0581 | — | — |
| [CORE-000102](../sdtm_rules/CORE-000102) | Published | Fully Executable | CG0428, TIG0582 | — | — |
| [CORE-000103](../sdtm_rules/CORE-000103) | Published | Fully Executable | CG0429, TIG0583 | — | — |
| [CORE-000104](../sdtm_rules/CORE-000104) | Published | Fully Executable | CG0430, TIG0584 | — | — |
| [CORE-000105](../sdtm_rules/CORE-000105) | Published | Fully Executable | CG0569, TIG0653 | FB2602 | — |
| [CORE-000106](../sdtm_rules/CORE-000106) | Published | Fully Executable | CG0045, TIG0324 | — | — |
| [CORE-000107](../sdtm_rules/CORE-000107) | Published | Fully Executable | CG0554, TIG0642 | — | — |
| [CORE-000108](../sdtm_rules/CORE-000108) | Published | Fully Executable | CG0133, TIG0382 | FB0602 | — |
| [CORE-000109](../sdtm_rules/CORE-000109) | Published | Fully Executable | CG0547 | — | — |
| [CORE-000110](../sdtm_rules/CORE-000110) | Published | Fully Executable | CG0549, TIG0637 | — | Note: Version 1 of rule CG0549 includes the --DRVFL variable. This will result in an overreporting when --STREFC is empty and --DRVFL = 'Y'. Completion of --STREFC is not dependent on --DRVFL completion only on completion of --ORREF. In a next version of the rule (version 2), this will be corrected. |
| [CORE-000111](../sdtm_rules/CORE-000111) | Published | Fully Executable | CG0564, TIG0649 | — | — |
| [CORE-000112](../sdtm_rules/CORE-000112) | Published | Fully Executable | CG0565, TIG0650 | — | — |
| [CORE-000113](../sdtm_rules/CORE-000113) | Published | Fully Executable | CG0566, TIG0651 | — | — |
| [CORE-000114](../sdtm_rules/CORE-000114) | Published | Fully Executable | CG0567, TIG0652 | — | — |
| [CORE-000115](../sdtm_rules/CORE-000115) | Published | Fully Executable | CG0570 | — | — |
| [CORE-000116](../sdtm_rules/CORE-000116) | Published | Fully Executable | CG0619, TIG0660 | — | — |
| [CORE-000117](../sdtm_rules/CORE-000117) | Published | Fully Executable | CG0081, TIG0346 | — | — |
| [CORE-000118](../sdtm_rules/CORE-000118) | Published | Fully Executable | CG0404, TIG0562 | — | — |
| [CORE-000119](../sdtm_rules/CORE-000119) | Published | Fully Executable | CG0521, TIG0616 | — | — |
| [CORE-000120](../sdtm_rules/CORE-000120) | Published | Fully Executable | CG0522, TIG0617 | — | — |
| [CORE-000121](../sdtm_rules/CORE-000121) | Published | Fully Executable | CG0520, TIG0615 | — | — |
| [CORE-000122](../sdtm_rules/CORE-000122) | Published | Fully Executable | CG0434, TIG0586 | — | — |
| [CORE-000123](../sdtm_rules/CORE-000123) | Published | Fully Executable | CG0388, TIG0550 | — | — |
| [CORE-000124](../sdtm_rules/CORE-000124) | Published | Fully Executable | CG0389, TIG0551 | — | — |
| [CORE-000125](../sdtm_rules/CORE-000125) | Published | Fully Executable | CG0390, TIG0552 | — | — |
| [CORE-000126](../sdtm_rules/CORE-000126) | Published | Fully Executable | CG0391, TIG0553 | — | — |
| [CORE-000127](../sdtm_rules/CORE-000127) | Published | Fully Executable | CG0392, TIG0554 | — | — |
| [CORE-000128](../sdtm_rules/CORE-000128) | Published | Fully Executable | CG0393, TIG0555 | — | — |
| [CORE-000129](../sdtm_rules/CORE-000129) | Published | Fully Executable | CG0394, TIG0556 | — | — |
| [CORE-000130](../sdtm_rules/CORE-000130) | Published | Fully Executable | CG0395, TIG0557 | — | — |
| [CORE-000131](../sdtm_rules/CORE-000131) | Published | Fully Executable | CG0396, TIG0558 | — | — |
| [CORE-000132](../sdtm_rules/CORE-000132) | Published | Fully Executable | CG0154, SEND213 | FB0914 | — |
| [CORE-000133](../sdtm_rules/CORE-000133) | Published | Fully Executable | CG0426, TIG0580 | — | — |
| [CORE-000134](../sdtm_rules/CORE-000134) | Published | Fully Executable | CG0203, TIG0423 | — | — |
| [CORE-000135](../sdtm_rules/CORE-000135) | Published | Fully Executable | CG0204, TIG0424 | — | — |
| [CORE-000136](../sdtm_rules/CORE-000136) | Published | Fully Executable | CG0201, TIG0422 | — | — |
| [CORE-000137](../sdtm_rules/CORE-000137) | Published | Fully Executable | CG0100, TIG0365 | — | — |
| [CORE-000138](../sdtm_rules/CORE-000138) | Published | Fully Executable | CG0221, TIG0435 | — | — |
| [CORE-000139](../sdtm_rules/CORE-000139) | Published | Fully Executable | CG0223, TIG0437 | — | — |
| [CORE-000140](../sdtm_rules/CORE-000140) | Published | Fully Executable | CG0225, TIG0438 | — | — |
| [CORE-000141](../sdtm_rules/CORE-000141) | Published | Fully Executable | CG0240, TIG0448 | FB0922 | — |
| [CORE-000142](../sdtm_rules/CORE-000142) | Published | Fully Executable | CG0241, TIG0449 | — | — |
| [CORE-000143](../sdtm_rules/CORE-000143) | Published | Fully Executable | CG0246, SEND24, TIG0165, TIG0450 | — | — |
| [CORE-000144](../sdtm_rules/CORE-000144) | Published | Fully Executable | CG0247, TIG0451 | — | — |
| [CORE-000145](../sdtm_rules/CORE-000145) | Published | Fully Executable | CG0255 | — | — |
| [CORE-000146](../sdtm_rules/CORE-000146) | Published | Fully Executable | CG0256 | — | — |
| [CORE-000147](../sdtm_rules/CORE-000147) | Published | Fully Executable | CG0257, SEND26, TIG0178, TIG0461 | — | — |
| [CORE-000148](../sdtm_rules/CORE-000148) | Published | Fully Executable | CG0258, TIG0462 | — | — |
| [CORE-000149](../sdtm_rules/CORE-000149) | Published | Fully Executable | CG0259 | — | — |
| [CORE-000150](../sdtm_rules/CORE-000150) | Published | Fully Executable | CG0260 | — | — |
| [CORE-000151](../sdtm_rules/CORE-000151) | Published | Fully Executable | CG0261, SEND281 | — | — |
| [CORE-000152](../sdtm_rules/CORE-000152) | Published | Fully Executable | CG0265, TIG0467 | — | — |
| [CORE-000153](../sdtm_rules/CORE-000153) | Published | Fully Executable | CG0266 | — | — |
| [CORE-000154](../sdtm_rules/CORE-000154) | Published | Fully Executable | CG0268, SEND246, TIG0167, TIG0470 | — | — |
| [CORE-000155](../sdtm_rules/CORE-000155) | Published | Fully Executable | CG0293, TIG0475 | — | — |
| [CORE-000156](../sdtm_rules/CORE-000156) | Published | Fully Executable | CG0294, TIG0476 | — | — |
| [CORE-000157](../sdtm_rules/CORE-000157) | Published | Fully Executable | CG0297, TIG0479 | — | — |
| [CORE-000158](../sdtm_rules/CORE-000158) | Published | Fully Executable | CG0163, TIG0396 | — | — |
| [CORE-000159](../sdtm_rules/CORE-000159) | Published | Fully Executable | CG0341, TIG0506 | — | — |
| [CORE-000160](../sdtm_rules/CORE-000160) | Published | Fully Executable | CG0342, TIG0507 | — | — |
| [CORE-000161](../sdtm_rules/CORE-000161) | Published | Fully Executable | CG0343, TIG0508 | — | — |
| [CORE-000162](../sdtm_rules/CORE-000162) | Published | Fully Executable | CG0344, TIG0509 | — | — |
| [CORE-000163](../sdtm_rules/CORE-000163) | Published | Fully Executable | CG0345, TIG0510 | — | — |
| [CORE-000164](../sdtm_rules/CORE-000164) | Published | Fully Executable | CG0346, TIG0511 | — | — |
| [CORE-000165](../sdtm_rules/CORE-000165) | Published | Fully Executable | CG0090, TIG0355 | FB3701 | — |
| [CORE-000166](../sdtm_rules/CORE-000166) | Published | Fully Executable | CG0091, TIG0356 | — | — |
| [CORE-000167](../sdtm_rules/CORE-000167) | Published | Fully Executable | CG0092, TIG0357 | — | — |
| [CORE-000168](../sdtm_rules/CORE-000168) | Published | Fully Executable | CG0034, TIG0315 | — | — |
| [CORE-000169](../sdtm_rules/CORE-000169) | Published | Partially Executable - Possible Overreporting | CG0185, TIG0414 | — | Explanation: This rule provides output when LBTOXGR does not contain only numeric values. But what this rule doesn't check is whether a numeric scale was used. This cannot be directly programmed from the --TOXGR content and should therefore be evaluated manually. |
| [CORE-000170](../sdtm_rules/CORE-000170) | Published | Fully Executable | CG0541, TIG0634 | — | — |
| [CORE-000171](../sdtm_rules/CORE-000171) | Published | Fully Executable | CG0058, TIG0332 | — | — |
| [CORE-000172](../sdtm_rules/CORE-000172) | Published | Fully Executable | CG0409, SEND249.1, TIG0168, TIG0565 | — | — |
| [CORE-000173](../sdtm_rules/CORE-000173) | Published | Fully Executable | CG0414, TIG0569 | — | — |
| [CORE-000174](../sdtm_rules/CORE-000174) | Published | Fully Executable | CG0356 | — | — |
| [CORE-000175](../sdtm_rules/CORE-000175) | Published | Fully Executable | CG0357 | — | — |
| [CORE-000176](../sdtm_rules/CORE-000176) | Published | Fully Executable | CG0358 | — | — |
| [CORE-000177](../sdtm_rules/CORE-000177) | Published | Fully Executable | CG0227, TIG0440 | — | — |
| [CORE-000178](../sdtm_rules/CORE-000178) | Published | Fully Executable | CG0172 | — | — |
| [CORE-000179](../sdtm_rules/CORE-000179) | Published | Fully Executable | CG0307, TIG0482 | FB0916 | — |
| [CORE-000180](../sdtm_rules/CORE-000180) | Published | Fully Executable | CG0308, TIG0483 | — | — |
| [CORE-000181](../sdtm_rules/CORE-000181) | Published | Fully Executable | CG0309 | — | — |
| [CORE-000182](../sdtm_rules/CORE-000182) | Published | Fully Executable | CG0310, SEND2, TIG0128, TIG0485 | — | — |
| [CORE-000183](../sdtm_rules/CORE-000183) | Published | Fully Executable | CG0318, TIG0489 | — | — |
| [CORE-000184](../sdtm_rules/CORE-000184) | Published | Fully Executable | CG0083, TIG0348 | FB0910 | — |
| [CORE-000185](../sdtm_rules/CORE-000185) | Published | Fully Executable | CG0123, TIG0380 | — | — |
| [CORE-000186](../sdtm_rules/CORE-000186) | Published | Fully Executable | CG0150, TIG0391 | — | — |
| [CORE-000187](../sdtm_rules/CORE-000187) | Published | Fully Executable | CG0168, TIG0400 | — | — |
| [CORE-000188](../sdtm_rules/CORE-000188) | Published | Fully Executable | CG0191 | — | — |
| [CORE-000189](../sdtm_rules/CORE-000189) | Published | Fully Executable | CG0665, TIG0699 | — | — |
| [CORE-000190](../sdtm_rules/CORE-000190) | Published | Fully Executable | CG0666, TIG0700 | — | — |
| [CORE-000191](../sdtm_rules/CORE-000191) | Published | Fully Executable | CG0529, TIG0622 | — | — |
| [CORE-000192](../sdtm_rules/CORE-000192) | Published | Fully Executable | CG0530, TIG0623 | — | — |
| [CORE-000193](../sdtm_rules/CORE-000193) | Published | Fully Executable | CG0503 | — | — |
| [CORE-000195](../sdtm_rules/CORE-000195) | Published | Fully Executable | CG0338, TIG0503 | — | — |
| [CORE-000196](../sdtm_rules/CORE-000196) | Published | Fully Executable | CG0337, TIG0502 | — | — |
| [CORE-000197](../sdtm_rules/CORE-000197) | Published | Fully Executable | CG0339, TIG0504 | — | — |
| [CORE-000198](../sdtm_rules/CORE-000198) | Published | Fully Executable | CG0340, TIG0505 | — | — |
| [CORE-000199](../sdtm_rules/CORE-000199) | Published | Fully Executable | CG0406, SEND64, TIG0563 | — | — |
| [CORE-000200](../sdtm_rules/CORE-000200) | Published | Fully Executable | CG0348, TIG0513 | — | — |
| [CORE-000201](../sdtm_rules/CORE-000201) | Published | Fully Executable | CG0029, SEND109, TIG0046, TIG0311 | — | — |
| [CORE-000202](../sdtm_rules/CORE-000202) | Published | Fully Executable | CG0419, TIG0574 | — | — |
| [CORE-000203](../sdtm_rules/CORE-000203) | Published | Fully Executable | CG0411, TIG0567 | — | — |
| [CORE-000204](../sdtm_rules/CORE-000204) | Published | Fully Executable | CG0410, TIG0566 | — | — |
| [CORE-000206](../sdtm_rules/CORE-000206) | Published | Fully Executable | CG0371, SEND121, TIG0058, TIG0535 | — | — |
| [CORE-000207](../sdtm_rules/CORE-000207) | Published | Fully Executable | CG0467, SEND78, TIG0276, TIG0597 | — | — |
| [CORE-000208](../sdtm_rules/CORE-000208) | Published | Partially Executable - Possible Overreporting | CG0512, TIG0607 | — | Explanation: The following part of the rule condition is not executable "Study does not use multi-stage arm assignments" and therefore cannot be included in the rule logic. As such the rule will also generate output for studies using multi-stage arm assignments. |
| [CORE-000209](../sdtm_rules/CORE-000209) | Published | Partially Executable - Possible Overreporting | CG0514, TIG0609 | — | Explanation: The following part of the rule condition is not executable "Study does not use multi-stage arm assignments" and therefore cannot be included in the rule logic. As such the rule will also generate output for studies using multi-stage arm assignments. |
| [CORE-000210](../sdtm_rules/CORE-000210) | Published | Partially Executable - Possible Overreporting | CG0516, TIG0611 | — | Explanation: The following part of the rule condition is not executable "Study does not use multi-stage arm assignments" and therefore cannot be included in the rule logic. As such the rule will also generate output for studies using multi-stage arm assignments. |
| [CORE-000211](../sdtm_rules/CORE-000211) | Published | Partially Executable - Possible Overreporting | CG0528 | — | — |
| [CORE-000212](../sdtm_rules/CORE-000212) | Published | Fully Executable | CG0535, TIG0628 | — | Note: To be evaluated for a next version: EPOCH to the output variables to support more efficient review and data issue detection. |
| [CORE-000213](../sdtm_rules/CORE-000213) | Published | Fully Executable | CG0536, TIG0629 | — | — |
| [CORE-000214](../sdtm_rules/CORE-000214) | Published | Fully Executable | CG0538, TIG0631 | — | — |
| [CORE-000215](../sdtm_rules/CORE-000215) | Published | Fully Executable | CG0539 | — | — |
| [CORE-000216](../sdtm_rules/CORE-000216) | Published | Fully Executable | CG0545 | — | — |
| [CORE-000217](../sdtm_rules/CORE-000217) | Published | Fully Executable | CG0462, TIG0592 | — | — |
| [CORE-000218](../sdtm_rules/CORE-000218) | Published | Fully Executable | CG0465, SEND118, TIG0055, TIG0595 | — | — |
| [CORE-000219](../sdtm_rules/CORE-000219) | Published | Fully Executable | CG0350, SEND44, TIG0515 | — | — |
| [CORE-000220](../sdtm_rules/CORE-000220) | Published | Fully Executable | CG0372, TIG0536 | — | — |
| [CORE-000221](../sdtm_rules/CORE-000221) | Published | Fully Executable | CG0417, TIG0572 | — | — |
| [CORE-000222](../sdtm_rules/CORE-000222) | Published | Fully Executable | CG0416, TIG0571 | — | — |
| [CORE-000223](../sdtm_rules/CORE-000223) | Published | Fully Executable | CG0513, TIG0608 | — | — |
| [CORE-000224](../sdtm_rules/CORE-000224) | Published | Fully Executable | CG0515, TIG0610 | — | — |
| [CORE-000225](../sdtm_rules/CORE-000225) | Published | Fully Executable | CG0094, TIG0359 | — | — |
| [CORE-000226](../sdtm_rules/CORE-000226) | Published | Fully Executable | CG0352 | — | — |
| [CORE-000227](../sdtm_rules/CORE-000227) | Published | Fully Executable | CG0178, TIG0407 | — | — |
| [CORE-000228](../sdtm_rules/CORE-000228) | Published | Fully Executable | CG0179, TIG0408 | — | — |
| [CORE-000229](../sdtm_rules/CORE-000229) | Published | Fully Executable | CG0361 | — | Note: There is an issue detected in the conformance rule as defined in the SDTM and SDTMIG v2.0 conformance rule spreadsheet. Class should be REL, not SPC. This has been noted in SDTMIGRULE-324. The CDISC Open Rule has been already implemented correctly with Class: RELATIONSHIP and Domain: RELSUB |
| [CORE-000230](../sdtm_rules/CORE-000230) | Published | Fully Executable | CG0362 | — | Note: There is an issue detected in the conformance rule as defined in the SDTM and SDTMIG v2.0 conformance rule spreadsheet. Class should be REL, not SPC. This has been noted in SDTMIGRULE-324. The CDISC Open Rule has been already implemented correctly with Class: RELATIONSHIP and Domain: RELSUB |
| [CORE-000231](../sdtm_rules/CORE-000231) | Published | Fully Executable | CG0363 | — | Note: There is an issue detected in the conformance rule as defined in the SDTM and SDTMIG v2.0 conformance rule spreadsheet. Class should be REL, not SPC. This has been noted in SDTMIGRULE-324. The CDISC Open Rule has been already implemented correctly with Class: RELATIONSHIP and Domain: RELSUB |
| [CORE-000232](../sdtm_rules/CORE-000232) | Published | Fully Executable | CG0364 | — | Note: There is an issue detected in the conformance rule as defined in the SDTM and SDTMIG v2.0 conformance rule spreadsheet. Class should be REL, not SPC. This has been noted in SDTMIGRULE-324. The CDISC Open Rule has been already implemented correctly with Class: RELATIONSHIP and Domain: RELSUB |
| [CORE-000233](../sdtm_rules/CORE-000233) | Published | Fully Executable | CG0365 | — | Note: CORE-000233 and CORE-00234 can be combined in a next release of the rules as the program logic is exactly the same for both rules |
| [CORE-000234](../sdtm_rules/CORE-000234) | Published | Fully Executable | CG0366 | — | Note: CORE-000233 and CORE-00234 can be combined in a next release of the rules as the program logic is exactly the same for both rules |
| [CORE-000235](../sdtm_rules/CORE-000235) | Published | Fully Executable | CG0367 | — | — |
| [CORE-000236](../sdtm_rules/CORE-000236) | Published | Fully Executable | CG0079, TIG0345 | — | — |
| [CORE-000237](../sdtm_rules/CORE-000237) | Published | Fully Executable | CG0027, SEND43, TIG0309 | — | — |
| [CORE-000238](../sdtm_rules/CORE-000238) | Published | Fully Executable | CG0147, TIG0388 | — | — |
| [CORE-000239](../sdtm_rules/CORE-000239) | Published | Fully Executable | CG0148, TIG0389 | — | — |
| [CORE-000240](../sdtm_rules/CORE-000240) | Published | Fully Executable | CG0420, TIG0575 | — | — |
| [CORE-000241](../sdtm_rules/CORE-000241) | Published | Fully Executable | CG0421, TIG0576 | — | — |
| [CORE-000242](../sdtm_rules/CORE-000242) | Published | Fully Executable | CG0353, TIG0518 | — | — |
| [CORE-000243](../sdtm_rules/CORE-000243) | Published | Fully Executable | CG0354, TIG0519 | — | — |
| [CORE-000244](../sdtm_rules/CORE-000244) | Published | Fully Executable | CG0355, TIG0520 | — | — |
| [CORE-000245](../sdtm_rules/CORE-000245) | Published | Fully Executable | CG0510, CG0635, TIG0605, TIG0676 | — | — |
| [CORE-000246](../sdtm_rules/CORE-000246) | Published | Fully Executable | CG0511, CG0636, TIG0606, TIG0677 | — | — |
| [CORE-000247](../sdtm_rules/CORE-000247) | Published | Fully Executable | CG0552, CG0626, TIG0640, TIG0667 | — | — |
| [CORE-000248](../sdtm_rules/CORE-000248) | Published | Fully Executable | CG0026, SEND63, TIG0265, TIG0308 | FB3702 | — |
| [CORE-000249](../sdtm_rules/CORE-000249) | Published | Fully Executable | CG0032, TIG0313 | — | — |
| [CORE-000250](../sdtm_rules/CORE-000250) | Published | Fully Executable | CG0078, TIG0344 | — | — |
| [CORE-000251](../sdtm_rules/CORE-000251) | Published | Fully Executable | CG0067 | FB0614 | — |
| [CORE-000252](../sdtm_rules/CORE-000252) | Published | Fully Executable | CG0136, TIG0385 | FB0605 | — |
| [CORE-000253](../sdtm_rules/CORE-000253) | Published | Fully Executable | CG0135, TIG0384 | FB0604 | — |
| [CORE-000254](../sdtm_rules/CORE-000254) | Published | Fully Executable | CG0134, TIG0383 | FB0603 | — |
| [CORE-000256](../sdtm_rules/CORE-000256) | Published | Fully Executable | CG0210, SEND125.1, TIG0062, TIG0429 | — | — |
| [CORE-000257](../sdtm_rules/CORE-000257) | Published | Fully Executable | CG0061, TIG0335 | FB4401 | — |
| [CORE-000258](../sdtm_rules/CORE-000258) | Published | Fully Executable | CG0062, TIG0336 | — | — |
| [CORE-000259](../sdtm_rules/CORE-000259) | Published | Fully Executable | CG0171 | FB0613 | — |
| [CORE-000260](../sdtm_rules/CORE-000260) | Published | Fully Executable | CG0085, TIG0350 | — | — |
| [CORE-000261](../sdtm_rules/CORE-000261) | Published | Fully Executable | CG0060, TIG0334 | — | — |
| [CORE-000262](../sdtm_rules/CORE-000262) | Published | Fully Executable | CG0226, TIG0439 | — | — |
| [CORE-000264](../sdtm_rules/CORE-000264) | Published | Partially Executable - Possible Overreporting | CG0039 | — | Explanation: Condition that primary SOC is used for the analysis cannot be programmatically checked so in case --BODSYS <> --SOC, then the condition should be checked. |
| [CORE-000265](../sdtm_rules/CORE-000265) | Published | Fully Executable | CG0046, TIG0325 | FB4402 | — |
| [CORE-000266](../sdtm_rules/CORE-000266) | Published | Fully Executable | CG0042, TIG0321 | — | — |
| [CORE-000267](../sdtm_rules/CORE-000267) | Published | Fully Executable | CG0050, TIG0328 | — | — |
| [CORE-000268](../sdtm_rules/CORE-000268) | Published | Fully Executable | CG0049, TIG0327 | FB0909 | — |
| [CORE-000269](../sdtm_rules/CORE-000269) | Published | Partially Executable - Possible Overreporting | CG0031, TIG0312 | — | Explanation: When SVPRESP is not present in the SV dataset (SDTMIG 3.2 and SDTMIG 3.3 SVPRESP is not an expected value), then this rule will overreport for unplanned visits as there is no way to distinguish which visits are planned and which are not. In case SVPRESP is included in the dataset (expected variable for SDTMIG 3.4), then only the planned visits will be compared with the VISITs in TV. |
| [CORE-000270](../sdtm_rules/CORE-000270) | Published | Partially Executable - Possible Overreporting | CG0033, TIG0314 | — | — |
| [CORE-000271](../sdtm_rules/CORE-000271) | Published | Fully Executable | CG0009, TIG0294 | — | — |
| [CORE-000272](../sdtm_rules/CORE-000272) | Published | Fully Executable | CG0336, SEND46, TIG0501 | — | — |
| [CORE-000289](../sdtm_rules/CORE-000289) | Published | Fully Executable | CG0181, TIG0410 | — | Note: Some assumptions where made to program this rule: 1) The interpretation of the guidance is that the rule applies when LBORRES is populated (not null). 2) Results listed as '< value' or '>v alue' are considered to be results lower or higher than quantification limits of a continuous measurement.<br>The rule logic applies until such time there is availability of reliable metadata to verify if the test is quantitative or not. |
| [CORE-000290](../sdtm_rules/CORE-000290) | Published | Fully Executable | CG0180, TIG0409 | — | Note: Some assumptions where made to program this rule: 1) The interpretation of the guidance is that the rule applies when LBORRES is populated (not null). 2) Results listed as '< value' or '>v alue' are considered to be results lower or higher than quantification limits of a continuous measurement.<br>The rule logic applies until such time there is availability of reliable metadata to verify if the test is quantitative or not. |
| [CORE-000291](../sdtm_rules/CORE-000291) | Published | Fully Executable | CG0105, TIG0370 | — | — |
| [CORE-000292](../sdtm_rules/CORE-000292) | Published | Fully Executable | CG0107 | — | — |
| [CORE-000293](../sdtm_rules/CORE-000293) | Published | Fully Executable | CG0205, TIG0425 | — | — |
| [CORE-000294](../sdtm_rules/CORE-000294) | Published | Fully Executable | CG0270, TIG0471 | — | — |
| [CORE-000295](../sdtm_rules/CORE-000295) | Published | Fully Executable | CG0550, TIG0638 | — | — |
| [CORE-000296](../sdtm_rules/CORE-000296) | Published | Fully Executable | CG0540, TIG0633 | — | — |
| [CORE-000297](../sdtm_rules/CORE-000297) | Published | Fully Executable | CG0501 | — | — |
| [CORE-000298](../sdtm_rules/CORE-000298) | Published | Fully Executable | CG0182, TIG0411 | — | Note: Some assumptions where made to program this rule: 1) The interpretation of the guidance is that the rule applies when LBORRES is populated (not null). 2) Results listed as '< value' or '>v alue' are considered to be results lower or higher than quantification limits of a continuous measurement.<br>The rule logic applies until such time there is availability of reliable metadata to verify if the test is quantitative or not. |
| [CORE-000299](../sdtm_rules/CORE-000299) | Published | Fully Executable | CG0183, TIG0412 | — | Note: Some assumptions where made to program this rule: 1) The interpretation of the guidance is that the rule applies when LBORRES is populated (not null). 2) Results listed as '< value' or '>v alue' are considered to be results lower or higher than quantification limits of a continuous measurement.<br>The rule logic applies until such time there is availability of reliable metadata to verify if the test is quantitative or not. |
| [CORE-000302](../sdtm_rules/CORE-000302) | Published | Partially Executable - Possible Overreporting | — | FB0920 | Explanation: This rule may overreport when long text values (>200 characters) are split across multiple SUPP-- records. In this scenario, the SDTM IG requires sequential QNAM values (e.g., DVTERM1, DVTERM2, ...) while retaining the same QLABEL for all records. Because the split records represent different segments of a single variable value rather than different variables, a one-to-one relationship between QNAM and QLABEL is not expected and repeated QLABEL values are valid. |
| [CORE-000303](../sdtm_rules/CORE-000303) | Published | Fully Executable | — | FB0901 | — |
| [CORE-000305](../sdtm_rules/CORE-000305) | Published | Fully Executable | — | FB4005 | — |
| [CORE-000308](../sdtm_rules/CORE-000308) | Published | Fully Executable | — | FB4002 | — |
| [CORE-000310](../sdtm_rules/CORE-000310) | Published | Fully Executable | — | FB4001 | — |
| [CORE-000318](../sdtm_rules/CORE-000318) | Published | Fully Executable | — | FB0902 | — |
| [CORE-000321](../sdtm_rules/CORE-000321) | Published | Fully Executable | — | FB3201 | — |
| [CORE-000322](../sdtm_rules/CORE-000322) | Published | Fully Executable | CG0066 | — | — |
| [CORE-000324](../sdtm_rules/CORE-000324) | Published | Fully Executable | CG0234, TIG0443 | — | — |
| [CORE-000326](../sdtm_rules/CORE-000326) | Published | Fully Executable | CG0568 | — | — |
| [CORE-000328](../sdtm_rules/CORE-000328) | Published | Fully Executable | — | FB3202 | — |
| [CORE-000329](../sdtm_rules/CORE-000329) | Published | Fully Executable | CG0063 | — | — |
| [CORE-000330](../sdtm_rules/CORE-000330) | Published | Fully Executable | CG0122 | — | — |
| [CORE-000331](../sdtm_rules/CORE-000331) | Published | Fully Executable | CG0124, CG0125 | — | — |
| [CORE-000332](../sdtm_rules/CORE-000332) | Published | Fully Executable | CG0193 | — | — |
| [CORE-000333](../sdtm_rules/CORE-000333) | Published | Partially Executable - Possible Overreporting | CG0215 | — | Explanation: This rule is applicable for SDTMIG v3.2 and v3.3 where the use of SVUPDES is permissible. SVPRESP planned versus unplanned visit was not yet introduced and this the permisisble variable SVUPDES was not standardly used (or info was not collected). In case the SVUPDES variable was not used to explain reason of an unplanned visit , then these unplanned visits will be reported in the ouput as these will not match visits in the TV dataset. |
| [CORE-000334](../sdtm_rules/CORE-000334) | Published | Fully Executable | CG0016, SEND13, TIG0065, TIG0301 | — | Note: This rule runs on the library metadata and therefore will provide output for the variables decribed in SDTMIG 3.3 - errata variables that should not have had core 'Expected': DSDY, LBSTREFC, MIBLFL, MOBLFL. |
| [CORE-000335](../sdtm_rules/CORE-000335) | Published | Fully Executable | CG0280 | — | — |
| [CORE-000337](../sdtm_rules/CORE-000337) | Published | Fully Executable | CG0140, TIG0386 | — | Note: Scope class/domain is set to Relationship/SUPPDM in the CORE rule iso SPC/DM in the conformance rule spreadsheet. This is due to the implemented check logic that starts from the condition in SUPPDM. |
| [CORE-000338](../sdtm_rules/CORE-000338) | Published | Fully Executable | CG0457 | — | — |
| [CORE-000339](../sdtm_rules/CORE-000339) | Published | Fully Executable | CG0456 | — | — |
| [CORE-000340](../sdtm_rules/CORE-000340) | Published | Fully Executable | CG0440 | — | — |
| [CORE-000348](../sdtm_rules/CORE-000348) | Published | Fully Executable | CG0076 | — | — |
| [CORE-000351](../sdtm_rules/CORE-000351) | Published | Partially Executable | CG0151, SEND37, TIG0255, TIG0392 | — | Explanation: Validation is done only within DM dataset within the data package. This rule is not checking uniqueness across a submission, only within a single trial. |
| [CORE-000352](../sdtm_rules/CORE-000352) | Published | Fully Executable | CG0207, SEND126, TIG0427 | — | — |
| [CORE-000354](../sdtm_rules/CORE-000354) | Published | Fully Executable | CG0007, TIG0292 | — | — |
| [CORE-000355](../sdtm_rules/CORE-000355) | Published | Fully Executable | CG0014, SEND12, TIG0057, TIG0299 | — | — |
| [CORE-000356](../sdtm_rules/CORE-000356) | Published | Fully Executable | CG0014, SEND12, TIG0057, TIG0299 | — | — |
| [CORE-000357](../sdtm_rules/CORE-000357) | Published | Fully Executable | CG0018, TIG0303 | — | — |
| [CORE-000358](../sdtm_rules/CORE-000358) | Published | Fully Executable | CG0022, TIG0306 | — | — |
| [CORE-000361](../sdtm_rules/CORE-000361) | Published | Fully Executable | CG0035, TIG0316 | FB0919 | — |
| [CORE-000362](../sdtm_rules/CORE-000362) | Published | Partially Executable - Possible Overreporting | CG0037 | — | Explanation: Condition that primary SOC is used for the analysis cannot be programmatically checked so in case --BDSYCD <> --SOCCD, then the condition should be checked. |
| [CORE-000363](../sdtm_rules/CORE-000363) | Published | Fully Executable | CG0068, TIG0338 | — | — |
| [CORE-000364](../sdtm_rules/CORE-000364) | Published | Fully Executable | CG0073 | — | — |
| [CORE-000365](../sdtm_rules/CORE-000365) | Published | Fully Executable | CG0077 | — | — |
| [CORE-000366](../sdtm_rules/CORE-000366) | Published | Fully Executable | CG0109 | — | — |
| [CORE-000367](../sdtm_rules/CORE-000367) | Published | Fully Executable | CG0117, CG0118 | — | — |
| [CORE-000368](../sdtm_rules/CORE-000368) | Published | Fully Executable | CG0120, CG0121 | — | — |
| [CORE-000369](../sdtm_rules/CORE-000369) | Published | Fully Executable | CG0141 | — | Note: The rule is programmed under the assumption that RFENDTC is used to define end of treatment. |
| [CORE-000370](../sdtm_rules/CORE-000370) | Published | Fully Executable | CG0143, TIG0387 | — | — |
| [CORE-000371](../sdtm_rules/CORE-000371) | Published | Fully Executable | CG0244 | — | — |
| [CORE-000372](../sdtm_rules/CORE-000372) | Published | Fully Executable | CG0269 | — | — |
| [CORE-000373](../sdtm_rules/CORE-000373) | Published | Fully Executable | CG0271 | — | — |
| [CORE-000374](../sdtm_rules/CORE-000374) | Published | Fully Executable | CG0537, TIG0630 | — | — |
| [CORE-000375](../sdtm_rules/CORE-000375) | Published | Fully Executable | CG0202 | — | — |
| [CORE-000376](../sdtm_rules/CORE-000376) | Published | Fully Executable | CG0349, TIG0514 | — | — |
| [CORE-000377](../sdtm_rules/CORE-000377) | Published | Fully Executable | CG0129 | — | — |
| [CORE-000378](../sdtm_rules/CORE-000378) | Published | Fully Executable | CG0142 | — | Note: The rule is programmed under the assumption that RFENDTC is used to define end of treatment. |
| [CORE-000379](../sdtm_rules/CORE-000379) | Published | Fully Executable | CG0145 | — | Note: The rule is programmed under the assumption that RFSTDTC is used to define start of treatment. |
| [CORE-000380](../sdtm_rules/CORE-000380) | Published | Fully Executable | CG0146 | — | Note: The rule is programmed under the assumption that RFSTDTC is used to define start of treatment. |
| [CORE-000384](../sdtm_rules/CORE-000384) | Published | Fully Executable | CG0374, TIG0538 | — | — |
| [CORE-000398](../sdtm_rules/CORE-000398) | Published | Fully Executable | CG0303, SEND276 | — | — |
| [CORE-000452](../sdtm_rules/CORE-000452) | Published | Fully Executable | CG0432 | — | — |
| [CORE-000453](../sdtm_rules/CORE-000453) | Published | Fully Executable | CG0433 | — | — |
| [CORE-000457](../sdtm_rules/CORE-000457) | Published | Fully Executable | CG0373, TIG0537 | — | — |
| [CORE-000467](../sdtm_rules/CORE-000467) | Published | Fully Executable | CG0441 | — | — |
| [CORE-000468](../sdtm_rules/CORE-000468) | Published | Fully Executable | CG0276 | — | — |
| [CORE-000469](../sdtm_rules/CORE-000469) | Published | Fully Executable | CG0277 | — | — |
| [CORE-000470](../sdtm_rules/CORE-000470) | Published | Fully Executable | CG0278 | — | — |
| [CORE-000473](../sdtm_rules/CORE-000473) | Published | Fully Executable | CG0272 | — | — |
| [CORE-000483](../sdtm_rules/CORE-000483) | Published | Fully Executable | CG0455 | FB1117 | **CG0455:** Note:<br>- CG0455 currently mentions NDF-RT but NDF-RT (National Drug File - Reference Terminology) was officially replaced by MED-RT (Medication Reference Terminology) in March 2018. The U.S. Veterans Health Administration (VHA) announced MED-RT as the successor to NDF-RT, with MED-RT becoming the authoritative terminology going forward. The CORE-000483 combining CG0445 and FDAB011 (FB1117) is programmed to check for MED-RT and not NDF-RT.<br>- In case the pharmalogical class is not yet defined and ‘NAV’ is entered in TSVALNF, then this rule will provide output which will need to be explained.<br><br>**FB1117:** Note: Rule CG0455 (combined with FB1117) currently mentions NDF-RT but NDF-RT (National Drug File - Reference Terminology) was officially replaced by MED-RT (Medication Reference Terminology) in March 2018. The U.S. Veterans Health Administration (VHA) announced MED-RT as the successor to NDF-RT, with MED-RT becoming the authoritative terminology going forward. The CORE-000483 combining CG0445 and FDAB011 (FB1117) is programmed to check for MED-RT and not NDF-RT. |
| [CORE-000484](../sdtm_rules/CORE-000484) | Published | Fully Executable | CG0200, TIG0421 | — | — |
| [CORE-000497](../sdtm_rules/CORE-000497) | Published | Partially Executable - Possible Overreporting | CG0279 | — | Explanation: In cases where the pharmalogical class is not yet defined and ‘NAV’ is entered in TSVALNF, then this rule will provide output which will need to be explained. |
| [CORE-000501](../sdtm_rules/CORE-000501) | Published | Fully Executable | CG0216 | — | — |
| [CORE-000502](../sdtm_rules/CORE-000502) | Published | Fully Executable | CG0369, TIG0533 | — | — |
| [CORE-000504](../sdtm_rules/CORE-000504) | Published | Fully Executable | CG0283 | — | — |
| [CORE-000505](../sdtm_rules/CORE-000505) | Published | Fully Executable | CG0285 | TRC1734c | — |
| [CORE-000506](../sdtm_rules/CORE-000506) | Published | Fully Executable | CG0286 | — | — |
| [CORE-000510](../sdtm_rules/CORE-000510) | Published | Fully Executable | CG0017 | — | — |
| [CORE-000515](../sdtm_rules/CORE-000515) | Published | Fully Executable | CG0412 | — | — |
| [CORE-000517](../sdtm_rules/CORE-000517) | Published | Fully Executable | — | FB4003 | — |
| [CORE-000518](../sdtm_rules/CORE-000518) | Published | Fully Executable | — | FB4004 | — |
| [CORE-000522](../sdtm_rules/CORE-000522) | Published | Fully Executable | — | FB1401 | — |
| [CORE-000527](../sdtm_rules/CORE-000527) | Published | Fully Executable | CG0209, TIG0428 | — | — |
| [CORE-000529](../sdtm_rules/CORE-000529) | Published | Fully Executable | CG0006, SEND73, SEND74, TIG0274, TIG0275, TIG0291 | FB1603 | — |
| [CORE-000530](../sdtm_rules/CORE-000530) | Published | Fully Executable | CG0119 | — | — |
| [CORE-000531](../sdtm_rules/CORE-000531) | Published | Fully Executable | CG0126, CG0128 | — | — |
| [CORE-000532](../sdtm_rules/CORE-000532) | Published | Fully Executable | CG0275 | — | — |
| [CORE-000533](../sdtm_rules/CORE-000533) | Published | Partially Executable - Possible Overreporting | CG0138 | — | Explanation: The rule checks population flags: COMPLT, FULLSET, ITT, PPROT, SAFETY based on the SDTMIG v3.2 Appendix C2 codelist. However, ADaM population flags aren't a fixed set and therefore this rule might not pick up all population flags that are in other SUPP-- domains than SUPPDM. |
| [CORE-000534](../sdtm_rules/CORE-000534) | Published | Fully Executable | CG0248, SEND221, TIG0148, TIG0452 | — | — |
| [CORE-000535](../sdtm_rules/CORE-000535) | Published | Fully Executable | CG0620, CG0662, SEND130, SEND130.1, TIG0066, TIG0661 | — | — |
| [CORE-000538](../sdtm_rules/CORE-000538) | Published | Fully Executable | CG0334, TIG0500 | — | — |
| [CORE-000539](../sdtm_rules/CORE-000539) | Published | Fully Executable | CG0332, TIG0498 | — | — |
| [CORE-000540](../sdtm_rules/CORE-000540) | Published | Fully Executable | CG0333, TIG0499 | — | — |
| [CORE-000541](../sdtm_rules/CORE-000541) | Published | Fully Executable | CG0372, TIG0536 | — | — |
| [CORE-000542](../sdtm_rules/CORE-000542) | Published | Fully Executable | SEND88, TIG0280 | FB3102 | — |
| [CORE-000543](../sdtm_rules/CORE-000543) | Published | Fully Executable | CG0127 | — | — |
| [CORE-000544](../sdtm_rules/CORE-000544) | Published | Fully Executable | CG0028 | — | Note: As per the SDTM and SDTMIG conformance rules v2.0 spreadsheet, the scope for Classes is 'ALL'. As this rule checks uniqueness of the --SEQ variable, relationship domains, trial design datasets and study reference where excluded in the check logic since these will not have a --SEQ variable or use --SEQ differently (OI dataset). This ha been noted in SDTMIGRULE-267 |
| [CORE-000550](../sdtm_rules/CORE-000550) | Published | Partially Executable - Possible Underreporting | CG0013, CG0351, TIG0298 | — | **CG0013:** Note: Columns in the library on 'usage restrictions' are not checked programmatically so these might not be picked up. These are normally picked up in separate conformance rules.<br>CG0013 is split into 2 CORE rules. CORE-000550 for SDTMIG 3.2 and SDTMIG 3.4. CORE-001079 is created for SDTMIG 3.3 only because certain allowed variables are not included in the library for Model 1.7: EXMETHOD, EGBEATNO, ICIMPLBL, MSAGENT, MSCONC, MSCONCU. These are hardcoded in the rule to avoid overreporting for this rule on these variables.<br>Explanation: Columns in the library on 'usage restrictions' are not checked programmatically so these might not be picked up. These are normally picked up in separate conformance rules.<br><br>**CG0351:** Explanation: Columns in the library on 'usage restrictions' are not checked programmatically so these might not be picked up. These are normally picked up in separate conformance rules. |
| [CORE-000552](../sdtm_rules/CORE-000552) | Published | Fully Executable | CG0220, TIG0434 | — | — |
| [CORE-000553](../sdtm_rules/CORE-000553) | Published | Fully Executable | CG0222, TIG0436 | — | — |
| [CORE-000562](../sdtm_rules/CORE-000562) | Published | Fully Executable | CG0273 | — | — |
| [CORE-000563](../sdtm_rules/CORE-000563) | Published | Fully Executable | CG0282 | — | — |
| [CORE-000564](../sdtm_rules/CORE-000564) | Published | Fully Executable | CG0458 | — | — |
| [CORE-000571](../sdtm_rules/CORE-000571) | Published | Fully Executable | CG0024, TIG0307 | — | — |
| [CORE-000572](../sdtm_rules/CORE-000572) | Published | Fully Executable | CG0235, TIG0444 | — | — |
| [CORE-000575](../sdtm_rules/CORE-000575) | Published | Partially Executable - Possible Underreporting | CG0219, SEND65, TIG0266, TIG0433 | — | Explanation: The engine retrieves the timing variables from the SDTM model linked to the SDTMIG version specified during the validation. However, the model has exceptions of timing variables not allowed in certain occassions like --DTC for Findings domains. This is listed as such in the library that the exception cannot be programmed. The rule might therefore underreport if one of the disallowed timing variables is used in the dataset. If this is the only timing variable used, the rule will consider this as correct. |
| [CORE-000579](../sdtm_rules/CORE-000579) | Published | Fully Executable | CG0408 | — | — |
| [CORE-000580](../sdtm_rules/CORE-000580) | Published | Fully Executable | CG0325, TIG0495 | — | — |
| [CORE-000581](../sdtm_rules/CORE-000581) | Published | Fully Executable | CG0368, TIG0532 | TRC1736a, TRC1736c | — |
| [CORE-000582](../sdtm_rules/CORE-000582) | Published | Fully Executable | CG0262 | — | — |
| [CORE-000585](../sdtm_rules/CORE-000585) | Published | Partially Executable - Possible Underreporting | CG0313 | — | Explanation: Scope of rule is limited to INTERVENTIONS, FINDINGS and EVENTS. This to avoid output for --SEQ, USUBJID variables in domains that don't need these variables. Although this rule is underreporting, all required and expected missing variables are covered in rules CG0014 (CORE-000355; CORE-000356), and CG0016 (CORE-000334) |
| [CORE-000586](../sdtm_rules/CORE-000586) | Published | Fully Executable | CG0398 | — | — |
| [CORE-000587](../sdtm_rules/CORE-000587) | Published | Fully Executable | CG0284 | — | — |
| [CORE-000594](../sdtm_rules/CORE-000594) | Published | Fully Executable | CG0359, SEND29, TIG0205, TIG0524 | — | Note: This rule only checks whether a variable label is in title case, as the conformance rule specifies. It does not check for absence of special characters. |
| [CORE-000597](../sdtm_rules/CORE-000597) | Published | Fully Executable | CG0043, TIG0322 | — | — |
| [CORE-000598](../sdtm_rules/CORE-000598) | Published | Fully Executable | CG0413, SEND1, TIG0037, TIG0568 | — | — |
| [CORE-000616](../sdtm_rules/CORE-000616) | Published | Fully Executable | — | FB4403 | — |
| [CORE-000642](../sdtm_rules/CORE-000642) | Published | Fully Executable | — | FB4404 | — |
| [CORE-000643](../sdtm_rules/CORE-000643) | Published | Fully Executable | — | FB2601 | — |
| [CORE-000655](../sdtm_rules/CORE-000655) | Published | Fully Executable | — | FB2501 | — |
| [CORE-000656](../sdtm_rules/CORE-000656) | Published | Fully Executable | — | FB2502 | — |
| [CORE-000657](../sdtm_rules/CORE-000657) | Published | Fully Executable | — | FB3409 | — |
| [CORE-000658](../sdtm_rules/CORE-000658) | Published | Fully Executable | — | FB3412 | — |
| [CORE-000659](../sdtm_rules/CORE-000659) | Published | Fully Executable | — | FB3410 | — |
| [CORE-000672](../sdtm_rules/CORE-000672) | Published | Fully Executable | — | FB3901 | — |
| [CORE-000675](../sdtm_rules/CORE-000675) | Published | Fully Executable | — | FB4201 | — |
| [CORE-000679](../sdtm_rules/CORE-000679) | Published | Fully Executable | — | FB0608 | — |
| [CORE-000685](../sdtm_rules/CORE-000685) | Published | Fully Executable | CG0571 | FB0923 | — |
| [CORE-000686](../sdtm_rules/CORE-000686) | Published | Fully Executable | CG0572 | FB0924 | — |
| [CORE-000689](../sdtm_rules/CORE-000689) | Published | Fully Executable | CG0573 | FB0925 | — |
| [CORE-000699](../sdtm_rules/CORE-000699) | Published | Fully Executable | — | FB3001 | — |
| [CORE-000700](../sdtm_rules/CORE-000700) | Published | Fully Executable | — | FB3204 | — |
| [CORE-000701](../sdtm_rules/CORE-000701) | Published | Partially Executable - Possible Overreporting | — | FB2201 | Explanation: In cases where observations are reported prior to the first informed consent date (e.g. prior medications) or in cases where EPOCHs cannot be assigned due to missing informaction, this rule will overreport and output will need to be explained. |
| [CORE-000705](../sdtm_rules/CORE-000705) | Published | Fully Executable | — | FB0610 | — |
| [CORE-000706](../sdtm_rules/CORE-000706) | Published | Fully Executable | — | FB0906 | — |
| [CORE-000707](../sdtm_rules/CORE-000707) | Published | Fully Executable | — | FB3208 | — |
| [CORE-000708](../sdtm_rules/CORE-000708) | Published | Fully Executable | — | FB3207 | — |
| [CORE-000709](../sdtm_rules/CORE-000709) | Published | Fully Executable | — | FB0607 | — |
| [CORE-000710](../sdtm_rules/CORE-000710) | Published | Fully Executable | CG0233, TIG0442 | — | — |
| [CORE-000711](../sdtm_rules/CORE-000711) | Published | Fully Executable | — | FB3404 | — |
| [CORE-000712](../sdtm_rules/CORE-000712) | Published | Fully Executable | CG0370, TIG0534 | — | — |
| [CORE-000713](../sdtm_rules/CORE-000713) | Published | Fully Executable | — | FB3411 | — |
| [CORE-000714](../sdtm_rules/CORE-000714) | Published | Fully Executable | — | FB3408 | — |
| [CORE-000716](../sdtm_rules/CORE-000716) | Published | Fully Executable | — | FB0911 | — |
| [CORE-000717](../sdtm_rules/CORE-000717) | Published | Fully Executable | — | FB3401 | — |
| [CORE-000718](../sdtm_rules/CORE-000718) | Published | Fully Executable | — | FB3209 | — |
| [CORE-000719](../sdtm_rules/CORE-000719) | Published | Fully Executable | — | FB0908 | — |
| [CORE-000720](../sdtm_rules/CORE-000720) | Published | Fully Executable | — | FB3406 | — |
| [CORE-000723](../sdtm_rules/CORE-000723) | Published | Fully Executable | — | FB0907 | — |
| [CORE-000726](../sdtm_rules/CORE-000726) | Published | Fully Executable | — | FB5701 | — |
| [CORE-000728](../sdtm_rules/CORE-000728) | Published | Fully Executable | — | FB0904 | — |
| [CORE-000729](../sdtm_rules/CORE-000729) | Published | Fully Executable | — | FB0912 | — |
| [CORE-000730](../sdtm_rules/CORE-000730) | Published | Fully Executable | CG0438 | — | — |
| [CORE-000731](../sdtm_rules/CORE-000731) | Published | Fully Executable | CG0439 | — | — |
| [CORE-000732](../sdtm_rules/CORE-000732) | Published | Fully Executable | — | FB3103 | — |
| [CORE-000733](../sdtm_rules/CORE-000733) | Published | Fully Executable | CG0281 | — | — |
| [CORE-000735](../sdtm_rules/CORE-000735) | Published | Fully Executable | CG0444 | FB1114 | — |
| [CORE-000736](../sdtm_rules/CORE-000736) | Published | Fully Executable | — | FB1116 | — |
| [CORE-000737](../sdtm_rules/CORE-000737) | Published | Fully Executable | — | FB1102 | — |
| [CORE-000738](../sdtm_rules/CORE-000738) | Published | Fully Executable | — | FB1106 | — |
| [CORE-000739](../sdtm_rules/CORE-000739) | Published | Partially Executable - Possible Overreporting | CG0407 | — | Explanation: Condition of this rule states 'Study includes protocol-specified study treatment'. This condition can not be programmed and therefore the rule will generate output for every study where the EX dataset is not present. In case where there is a valid reason EX dataset is not needed, rule output should be explained. |
| [CORE-000740](../sdtm_rules/CORE-000740) | Published | Fully Executable | CG0287 | — | — |
| [CORE-000743](../sdtm_rules/CORE-000743) | Published | Fully Executable | — | FB0918 | — |
| [CORE-000744](../sdtm_rules/CORE-000744) | Published | Fully Executable | CG0174, TIG0403 | — | — |
| [CORE-000745](../sdtm_rules/CORE-000745) | Published | Fully Executable | — | FB0915 | — |
| [CORE-000748](../sdtm_rules/CORE-000748) | Published | Partially Executable - Possible Overreporting | — | FB2504 | Explanation: The FDA guidance indicates that: Randomized subjects are expected to receive a study treatment. This rule is therefore programmed on randomization (ARMNRS) In cases where subjects are randomized but not treated (ARMNRS = ASSIGNED, NOT TREATED or UNPLANNED TREATMENT), this rule will overreport. |
| [CORE-000757](../sdtm_rules/CORE-000757) | Published | Fully Executable | CG0602, TIG0656 | — | — |
| [CORE-000758](../sdtm_rules/CORE-000758) | Published | Fully Executable | CG0534, TIG0627 | — | Note: The rule is programmed under the assumption that RFSTDTC is used to define start of treatment. |
| [CORE-000760](../sdtm_rules/CORE-000760) | Published | Fully Executable | — | FB3413 | — |
| [CORE-000761](../sdtm_rules/CORE-000761) | Published | Fully Executable | CG0289 | — | — |
| [CORE-000763](../sdtm_rules/CORE-000763) | Published | Fully Executable | CG0232, TIG0441 | — | — |
| [CORE-000765](../sdtm_rules/CORE-000765) | Published | Fully Executable | — | FB2401 | — |
| [CORE-000766](../sdtm_rules/CORE-000766) | Published | Fully Executable | CG0601 | — | — |
| [CORE-000767](../sdtm_rules/CORE-000767) | Published | Fully Executable | CG0603 | — | — |
| [CORE-000774](../sdtm_rules/CORE-000774) | Published | Partially Executable - Possible Overreporting | — | FB4202 | Note: This rule is programmed as stated in the FDA business rule: When a test is not done, the result variable should not be populated, and the reason not done should be provided in the appropriate variable.<br>There are occassions where the 'reason not done' is not collected and these will be present in the rule output. These cases need to be explained. |
| [CORE-000776](../sdtm_rules/CORE-000776) | Published | Fully Executable | — | FB3203 | — |
| [CORE-000777](../sdtm_rules/CORE-000777) | Published | Fully Executable | CG0502 | — | — |
| [CORE-000778](../sdtm_rules/CORE-000778) | Published | Fully Executable | CG0650 | — | — |
| [CORE-000779](../sdtm_rules/CORE-000779) | Published | Fully Executable | CG0376 | — | — |
| [CORE-000783](../sdtm_rules/CORE-000783) | Published | Fully Executable | CG0314, SEND274, SEND274.1 | — | — |
| [CORE-000784](../sdtm_rules/CORE-000784) | Published | Partially Executable - Possible Overreporting | CG0217, TIG0431 | — | Explanation: When SVSTDTC falls right on a tie between 2 TAETORDs, then it will validate the TAETORD of SV against both TAETORDss in SE. This will result in output that needs to be explained based on tie breakers defined on trial level. |
| [CORE-000785](../sdtm_rules/CORE-000785) | Published | Fully Executable | CG0429, TIG0583 | — | — |
| [CORE-000786](../sdtm_rules/CORE-000786) | Published | Fully Executable | CG0430, TIG0584 | — | — |
| [CORE-000787](../sdtm_rules/CORE-000787) | Published | Fully Executable | CG0291 | — | — |
| [CORE-000790](../sdtm_rules/CORE-000790) | Published | Partially Executable - Possible Overreporting | — | FB2505 | Explanation: The FDA guidance indicates that: Randomized subjects are expected to receive a study treatment. This rule is therefore programmed on randomization (ARM) and not on actual treatment (ACTARM). In cases where subjects are randomized but not treated, this rule will overreport. |
| [CORE-000791](../sdtm_rules/CORE-000791) | Published | Fully Executable | — | FB0903 | — |
| [CORE-000792](../sdtm_rules/CORE-000792) | Published | Fully Executable | — | FB0905 | — |
| [CORE-000793](../sdtm_rules/CORE-000793) | Published | Fully Executable | — | FB1601 | — |
| [CORE-000841](../sdtm_rules/CORE-000841) | Published | Fully Executable | — | FB0612 | — |
| [CORE-000842](../sdtm_rules/CORE-000842) | Published | Fully Executable | CG0213 | — | Note: In case this rule provides output for visits are unplanned but SVUPDES is not present in the dataset or not populated, in that case it is recommended to add a Description of what happened to the subject during an unplanned visit in SVUPDES as per SDTM IG. |
| [CORE-000843](../sdtm_rules/CORE-000843) | Published | Fully Executable | CG0214 | — | — |
| [CORE-000844](../sdtm_rules/CORE-000844) | Published | Fully Executable | CG0531 | — | — |
| [CORE-000845](../sdtm_rules/CORE-000845) | Published | Fully Executable | CG0531 | — | — |
| [CORE-000846](../sdtm_rules/CORE-000846) | Published | Fully Executable | CG0531 | — | — |
| [CORE-000852](../sdtm_rules/CORE-000852) | Published | Fully Executable | CG0330, CG0664, SEND48, TIG0698 | — | — |
| [CORE-000853](../sdtm_rules/CORE-000853) | Published | Fully Executable | — | FB1602 | — |
| [CORE-000862](../sdtm_rules/CORE-000862) | Published | Fully Executable | — | FB3205 | — |
| [CORE-000863](../sdtm_rules/CORE-000863) | Published | Fully Executable | — | FB3101 | — |
| [CORE-000864](../sdtm_rules/CORE-000864) | Published | Fully Executable | — | FB3206 | — |
| [CORE-000865](../sdtm_rules/CORE-000865) | Published | Fully Executable | — | FB4405 | — |
| [CORE-000866](../sdtm_rules/CORE-000866) | Published | Fully Executable | — | FB3210 | — |
| [CORE-000867](../sdtm_rules/CORE-000867) | Published | Fully Executable | — | FB1501 | — |
| [CORE-000880](../sdtm_rules/CORE-000880) | Published | Fully Executable | — | FB4006 | — |
| [CORE-000885](../sdtm_rules/CORE-000885) | Published | Fully Executable | — | FB2302 | — |
| [CORE-000886](../sdtm_rules/CORE-000886) | Published | Fully Executable | — | FB2306 | — |
| [CORE-000887](../sdtm_rules/CORE-000887) | Published | Fully Executable | — | FB2301 | — |
| [CORE-000889](../sdtm_rules/CORE-000889) | Published | Partially Executable - Possible Underreporting | — | FB3902 | — |
| [CORE-000890](../sdtm_rules/CORE-000890) | Published | Fully Executable | — | FB1502 | — |
| [CORE-000892](../sdtm_rules/CORE-000892) | Published | Fully Executable | — | FB4301 | — |
| [CORE-000901](../sdtm_rules/CORE-000901) | Published | Partially Executable - Possible Underreporting | — | FB6901 | Explanation: RELREC between PC and PP is not obliged. So if there is a RELREC between PP and PC then the linking can be done on RFTDTC. But if not, then the rule can only check if the value for PCCAT exists in PC as a PCTEST for that subject. That part is not programmed. Rule will only work when RELREC is created. |
| [CORE-000913](../sdtm_rules/CORE-000913) | Published | Fully Executable | — | FB0611 | — |
| [CORE-000914](../sdtm_rules/CORE-000914) | Published | Fully Executable | — | FB2603 | — |
| [CORE-000915](../sdtm_rules/CORE-000915) | Published | Fully Executable | — | FB2604 | — |
| [CORE-000916](../sdtm_rules/CORE-000916) | Published | Fully Executable | CG0370, TIG0534 | — | — |
| [CORE-000927](../sdtm_rules/CORE-000927) | Published | Fully Executable | — | FB2304 | — |
| [CORE-000929](../sdtm_rules/CORE-000929) | Published | Fully Executable | CG0001, SEND16, TIG0090, TIG0289 | — | — |
| [CORE-000952](../sdtm_rules/CORE-000952) | Published | Fully Executable | — | FB3407 | — |
| [CORE-000953](../sdtm_rules/CORE-000953) | Published | Fully Executable | CG0370, TIG0534 | — | — |
| [CORE-001034](../sdtm_rules/CORE-001034) | Published | Fully Executable | CG0562, TIG0648 | — | — |
| [CORE-001043](../sdtm_rules/CORE-001043) | Published | Fully Executable | — | FB0501 | — |
| [CORE-001064](../sdtm_rules/CORE-001064) | Published | Fully Executable | — | FB2305 | — |
| [CORE-001078](../sdtm_rules/CORE-001078) | Published | Fully Executable | — | FB0609 | — |
| [CORE-001079](../sdtm_rules/CORE-001079) | Published | Partially Executable - Possible Underreporting | CG0013, CG0351 | — | **CG0013:** Note: Columns in the library on 'usage restrictions' are not checked programmatically so these might not be picked up. These are normally picked up in separate conformance rules.<br>CG0013 is split into 2 CORE rules. CORE-000550 for SDTMIG 3.2 and SDTMIG 3.4. CORE-001079 is created for SDTMIG 3.3 only because certain allowed variables are not included in the library for Model 1.7: EXMETHOD, EGBEATNO, ICIMPLBL, MSAGENT, MSCONC, MSCONCU. These are hardcoded in the rule to avoid overreporting for this rule on these variables.<br>Explanation: Columns in the library on 'usage restrictions' are not checked programmatically so these might not be picked up. These are normally picked up in separate conformance rules.<br><br>**CG0351:** Explanation: Columns in the library on 'usage restrictions' are not checked programmatically so these might not be picked up. These are normally picked up in separate conformance rules. |
| [CORE-001080](../sdtm_rules/CORE-001080) | Published | Fully Executable | CG0288 | — | — |
| [CORE-001081](../sdtm_rules/CORE-001081) | Published | Fully Executable | CG0010 | — | — |
| [CORE-001082](../sdtm_rules/CORE-001082) | Published | Partially Executable - Possible Overreporting | CG0012 | — | Note: This rule will report for all variables that are not in the library for the domain, class and model version used by the SDTMIG used to build the datasets (e.g. SESTDY for SDTMIG3.3 or SUBJID for SDTMIG 3.3, 3.4). Because there is no real reference to check whether the variable type is correctly used for these newly added variables, the output should be checked and explained why this is the correct datatype for these variables. |
| [CORE-002000](../sdtm_rules/CORE-002000) | Published | Fully Executable | CG0464 | — | — |
| [CORE-002001](../sdtm_rules/CORE-002001) | Published | Fully Executable | CG0002 | — | — |
| [CORE-002002](../sdtm_rules/CORE-002002) | Published | Fully Executable | CG0320 | — | — |
| [CORE-002003](../sdtm_rules/CORE-002003) | Published | Fully Executable | CG0463 | — | — |
| [CORE-002004](../sdtm_rules/CORE-002004) | Published | Fully Executable | CG0097 | — | — |
| [CORE-002005](../sdtm_rules/CORE-002005) | Published | Fully Executable | CG0312 | — | — |
| [CORE-002006](../sdtm_rules/CORE-002006) | Published | Fully Executable | CG0015 | — | — |
| [CORE-002007](../sdtm_rules/CORE-002007) | Published | Fully Executable | CG0019 | — | — |
| [CORE-002008](../sdtm_rules/CORE-002008) | Published | Fully Executable | CG0377 | FB1707 | Note: Rule is written to also pick up cases where the --LLT variable is empty. Assumption is made that in case --LLT variable is added to the dataset, that it is expected to be completed. In rare cases where only certain events are coded, and --LLT is not expected to be completed for certain data points, then this rule could overreport. As this is unlikely to happen, rule is kept as 'fully executable'. |
| [CORE-002009](../sdtm_rules/CORE-002009) | Published | Fully Executable | CG0378 | — | Note: Rule is written to also pick up cases where the --LLTCD variable is empty. Assumption is made that in case --LLTCD variable is added to the dataset, that it is expected to be completed. In rare cases where only certain events are coded, and --LLTCD is not expected to be completed for certain data points, then this rule could overreport. As this is unlikely to happen, rule is kept as 'fully executable'. |
| [CORE-002010](../sdtm_rules/CORE-002010) | Published | Fully Executable | CG0380 | — | — |
| [CORE-002011](../sdtm_rules/CORE-002011) | Published | Fully Executable | CG0382 | — | — |
| [CORE-002012](../sdtm_rules/CORE-002012) | Published | Fully Executable | CG0384 | — | — |
| [CORE-002013](../sdtm_rules/CORE-002013) | Published | Fully Executable | CG0381 | FB1708 | — |
| [CORE-002014](../sdtm_rules/CORE-002014) | Published | Fully Executable | CG0383 | FB1709 | — |
| [CORE-002015](../sdtm_rules/CORE-002015) | Published | Fully Executable | CG0379 | FB1704 | — |
| [CORE-002016](../sdtm_rules/CORE-002016) | Published | Fully Executable | CG0546 | — | — |
| [CORE-002017](../sdtm_rules/CORE-002017) | Published | Fully Executable | — | FB0401 | Note: Scope of rule is set to 'ALL' because it needs to scan all domains in the define-xml document |
| [CORE-002018](../sdtm_rules/CORE-002018) | Published | Fully Executable | — | FB0402 | Note: Scope of rule is set to 'ALL' because it needs to scan all domains in the define-xml document |
| [CORE-002019](../sdtm_rules/CORE-002019) | Published | Fully Executable | — | FB0403 | Note: Scope of rule is set to 'ALL' because it needs to scan all domains in the define-xml document |
| [CORE-002020](../sdtm_rules/CORE-002020) | Published | Fully Executable | — | FB0404 | Note: Scope of rule is set to 'ALL' because it needs to scan all domains in the define-xml document |
| [CORE-002021](../sdtm_rules/CORE-002021) | Published | Fully Executable | — | FB0405 | Note: Scope of rule is set to 'ALL' because it needs to scan all domains in the define-xml document |
| [CORE-002022](../sdtm_rules/CORE-002022) | Published | Fully Executable | — | FB0406 | Note: Scope of rule is set to 'ALL' because it needs to scan all domains in the define-xml document |
| [CORE-002023](../sdtm_rules/CORE-002023) | Published | Fully Executable | — | FB0407 | Note: Scope of rule is set to 'ALL' because it needs to scan all domains in the define-xml document |
| [CORE-002024](../sdtm_rules/CORE-002024) | Published | Fully Executable | — | FB0408 | Note: Scope of rule is set to 'ALL' because it needs to scan all domains in the define-xml document |
| [CORE-002025](../sdtm_rules/CORE-002025) | Published | Fully Executable | — | FB0409 | Note: Scope of rule is set to 'ALL' because it needs to scan all domains in the define-xml document |
| [CORE-002026](../sdtm_rules/CORE-002026) | Published | Fully Executable | — | FB0410 | Note: Scope of rule is set to 'ALL' because it needs to scan all domains in the define-xml document |
| [CORE-002027](../sdtm_rules/CORE-002027) | Published | Fully Executable | — | FB0411 | Note: Scope of rule is set to 'ALL' because it needs to scan all domains in the define-xml document |
| [CORE-002028](../sdtm_rules/CORE-002028) | Published | Fully Executable | — | FB0412 | Note: Scope of rule is set to 'ALL' because it needs to scan all domains in the define-xml document |
| [CORE-002029](../sdtm_rules/CORE-002029) | Published | Fully Executable | — | FB0413 | Note: Scope of rule is set to 'ALL' because it needs to scan all domains in the define-xml document |
| [CORE-002030](../sdtm_rules/CORE-002030) | Published | Fully Executable | CG0431 | — | — |
| [CORE-002031](../sdtm_rules/CORE-002031) | Published | Fully Executable | CG0386 | — | — |
| [CORE-002032](../sdtm_rules/CORE-002032) | Published | Fully Executable | — | FB0801 | — |
| [CORE-002033](../sdtm_rules/CORE-002033) | Published | Fully Executable | — | FB0802 | — |
| [CORE-002034](../sdtm_rules/CORE-002034) | Published | Fully Executable | — | FB0101 | — |
| [CORE-002035](../sdtm_rules/CORE-002035) | Published | Fully Executable | — | FB4303 | — |
| [CORE-002036](../sdtm_rules/CORE-002036) | Published | Fully Executable | — | FB4304 | — |
| [CORE-002037](../sdtm_rules/CORE-002037) | Published | Fully Executable | — | FB0926 | — |
| [CORE-002038](../sdtm_rules/CORE-002038) | Published | Partially Executable - Possible Overreporting | — | FB2503 | Explanation: The FDA guidance indicates that: Randomized subjects are expected to receive a study treatment. This rule is therefore programmed on randomization (ARMCD) and not on actual treatment (ACTARMCD). In cases where subjects are randomized but not treated, this rule will overreport. |
| [CORE-002039](../sdtm_rules/CORE-002039) | Published | Fully Executable | — | FB4302 | — |
| [CORE-002040](../sdtm_rules/CORE-002040) | Published | Fully Executable | CG0321 | — | Note: Conformance rule indicates that scope is ALL classes and ALL domains. To avoid this rule to overreport for relationship domains as these are allowed for custom domains, SUPP-- is excluded from CORE-002040. |
| [CORE-002041](../sdtm_rules/CORE-002041) | Published | Fully Executable | — | FB0301 | — |
| [CORE-002042](../sdtm_rules/CORE-002042) | Published | Fully Executable | CG0555 | — | — |
| [CORE-002043](../sdtm_rules/CORE-002043) | Published | Fully Executable | CG0556 | — | — |
| [CORE-002044](../sdtm_rules/CORE-002044) | Published | Fully Executable | CG0557 | — | — |
| [CORE-002045](../sdtm_rules/CORE-002045) | Published | Fully Executable | CG0558 | — | — |
| [CORE-002046](../sdtm_rules/CORE-002046) | Published | Fully Executable | CG0559 | — | — |
| [CORE-002047](../sdtm_rules/CORE-002047) | Published | Fully Executable | CG0385 | FB1705 | — |
| [CORE-002048](../sdtm_rules/CORE-002048) | Published | Fully Executable | CG0560 | — | — |
| [CORE-002049](../sdtm_rules/CORE-002049) | Published | Fully Executable | — | FB3214 | — |
| [CORE-002050](../sdtm_rules/CORE-002050) | Published | Fully Executable | — | FB1103 | — |
| [CORE-002051](../sdtm_rules/CORE-002051) | Published | Fully Executable | — | FB1104 | — |
| [CORE-002052](../sdtm_rules/CORE-002052) | Published | Fully Executable | — | FB1711 | — |
| [CORE-002053](../sdtm_rules/CORE-002053) | Published | Fully Executable | — | FB4305 | — |
| [CORE-002054](../sdtm_rules/CORE-002054) | Published | Fully Executable | — | FB4306 | — |
| [CORE-002055](../sdtm_rules/CORE-002055) | Published | Fully Executable | — | FB3601 | — |
| [CORE-002056](../sdtm_rules/CORE-002056) | Published | Partially Executable - Possible Overreporting | — | FB1101 | Note: This rule will also flag missing TD and TM domains. As per FDA TCG: all TDM datasets should be included with each SDTM study submission to describe the planned conduct of a clinical study.<br>This is exactly what this rule is checking but TD and TM are only applicable in certain cases and an explanation should be added as to why these datasets are not included. |
| [CORE-002057](../sdtm_rules/CORE-002057) | Published | Fully Executable | — | FB1105 | — |
| [CORE-002058](../sdtm_rules/CORE-002058) | Published | Fully Executable | — | FB1107 | — |
| [CORE-002059](../sdtm_rules/CORE-002059) | Published | Fully Executable | — | FB1108 | — |
| [CORE-002060](../sdtm_rules/CORE-002060) | Published | Fully Executable | — | FB1713 | — |
| [CORE-002061](../sdtm_rules/CORE-002061) | Published | Fully Executable | — | FB1801 | — |
| [CORE-002062](../sdtm_rules/CORE-002062) | Published | Fully Executable | — | FB1901 | — |
| [CORE-002063](../sdtm_rules/CORE-002063) | Published | Fully Executable | CG0445 | FB1115 | — |
| [CORE-002064](../sdtm_rules/CORE-002064) | Published | Fully Executable | CG0450 | FB1115 | — |
| [CORE-002065](../sdtm_rules/CORE-002065) | Published | Fully Executable | CG0442 | FB1115 | — |
| [CORE-002066](../sdtm_rules/CORE-002066) | Published | Fully Executable | CG0454 | FB1119 | — |
| [CORE-002067](../sdtm_rules/CORE-002067) | Published | Fully Executable | CG0453 | FB1118 | — |
| [CORE-002068](../sdtm_rules/CORE-002068) | Published | Fully Executable | CG0451 | FB1116 | — |
| [CORE-002069](../sdtm_rules/CORE-002069) | Published | Fully Executable | CG0443 | FB1116 | — |
| [CORE-002070](../sdtm_rules/CORE-002070) | Published | Fully Executable | CG0446 | FB1116 | — |
| [CORE-002071](../sdtm_rules/CORE-002071) | Published | Fully Executable | CG0449 | FB1122 | — |
| [CORE-002072](../sdtm_rules/CORE-002072) | Published | Fully Executable | CG0448 | FB1121 | — |
| [CORE-002073](../sdtm_rules/CORE-002073) | Published | Fully Executable | CG0436 | FB1706 | — |
| [CORE-002074](../sdtm_rules/CORE-002074) | Published | Fully Executable | CG0437 | — | — |
| [CORE-002075](../sdtm_rules/CORE-002075) | Published | Fully Executable | — | FB1703 | — |
| [CORE-002076](../sdtm_rules/CORE-002076) | Published | Fully Executable | — | FB3211 | — |
| [CORE-002077](../sdtm_rules/CORE-002077) | Published | Fully Executable | — | FB3801 | — |
| [CORE-002078](../sdtm_rules/CORE-002078) | Published | Fully Executable | — | FB3212 | — |
| [CORE-002079](../sdtm_rules/CORE-002079) | Published | Fully Executable | — | FB3402 | — |
| [CORE-002080](../sdtm_rules/CORE-002080) | Published | Fully Executable | — | FB1109 | — |
| [CORE-002081](../sdtm_rules/CORE-002081) | Published | Fully Executable | — | FB1110 | — |
| [CORE-002082](../sdtm_rules/CORE-002082) | Published | Fully Executable | — | FB1111 | — |
| [CORE-002083](../sdtm_rules/CORE-002083) | Published | Fully Executable | — | FB1112 | — |
| [CORE-002084](../sdtm_rules/CORE-002084) | Published | Fully Executable | — | TRC1736b | — |
| [CORE-002085](../sdtm_rules/CORE-002085) | Published | Fully Executable | — | TRC1734b | — |
| [CORE-002086](../sdtm_rules/CORE-002086) | Published | Fully Executable | — | FB5801 | — |
| [CORE-002087](../sdtm_rules/CORE-002087) | Published | Fully Executable | — | FB3414 | — |
| [CORE-002088](../sdtm_rules/CORE-002088) | Published | Fully Executable | — | FB3405 | — |
| [CORE-002089](../sdtm_rules/CORE-002089) | Published | Fully Executable | — | FB3403 | — |
| [CORE-002090](../sdtm_rules/CORE-002090) | Published | Fully Executable | — | FB2303 | — |
| [CORE-002091](../sdtm_rules/CORE-002091) | Published | Fully Executable | — | FB3213 | — |
| [CORE-002092](../sdtm_rules/CORE-002092) | Published | Fully Executable | — | FB1712 | — |
| [CORE-002093](../sdtm_rules/CORE-002093) | Published | Fully Executable | — | FB5901 | — |
| [CORE-002094](../sdtm_rules/CORE-002094) | Published | Fully Executable | — | FB7001 | — |
| [CORE-002095](../sdtm_rules/CORE-002095) | Published | Fully Executable | — | TRC1734a | — |
| [CORE-002096](../sdtm_rules/CORE-002096) | Published | Fully Executable | — | FB5501 | — |
| [CORE-002097](../sdtm_rules/CORE-002097) | Published | Fully Executable | — | FB6001 | — |
| [CORE-002098](../sdtm_rules/CORE-002098) | Published | Fully Executable | CG0184 | — | Note: Some assumptions where made to program this rule: 1) The interpretation of the guidance is that the rule applies when LBORRES is populated (not null). 2) Results listed as '< value' or '>v alue' are considered to be results lower or higher than quantification limits of a continuous measurement.<br>The rule logic applies until such time there is availability of reliable metadata to verify if the test is quantitative or not. |
| [CORE-002099](../sdtm_rules/CORE-002099) | Published | Fully Executable | CG0524 | — | — |
| [CORE-002100](../sdtm_rules/CORE-002100) | Published | Fully Executable | CG0532 | — | Note: The rule is programmed under the assumption that RFSTDTC is used to define start of treatment. |
| [CORE-002101](../sdtm_rules/CORE-002101) | Published | Fully Executable | CG0418 | — | — |
| [CORE-002102](../sdtm_rules/CORE-002102) | Published | Partially Executable - Possible Underreporting | CG0267 | — | Note: Condition of the rule states: "Reference Terminology is versioned.". The rule is now programmed to check this for commonly known reference terminology in TS: CDISC CT, UNII, SNOMED and MED-RT. Any additional reference terminology included in TS that is versioned is not check in this rule and should be addressed manually. |
| [CORE-002103](../sdtm_rules/CORE-002103) | Published | Fully Executable | CG0096 | FB1710 | Note: Condition as specified is difficult to program due to the fact that CMTRT is a free text field: "CMTRT has a decode value in the dictionary". Feedback has been requested: https://jira.cdisc.org/browse/SDTMIGRULE-320<br>But in a meanwhile, rule will be programmed like this: CMDECOD is being checked for a valid value in WHODD |
| [CORE-002104](../sdtm_rules/CORE-002104) | Published | Fully Executable | — | FB4307 | — |
| [CORE-002105](../sdtm_rules/CORE-002105) | Published | Fully Executable | — | FB7101 | — |
| [CORE-002106](../sdtm_rules/CORE-002106) | Published | Fully Executable | CG0011 | — | Note: Rule CG0011 specifies: Variable Format = SDTM-specified controlled terminology and format guidelines for variables, when provided. Due to the generic nature of the rule, it was split into 6 parts.<br>- CORE-002106: Part A - Raise an error when value for COUNTRY in DM dataset is not populated with a valid 3-letter country code found in ISO 3166-1.<br>- CORE-002119: Part B - Raise an error when --EVLINT is not ISO 8601 duration or interval.<br>- CORE-002113: Part C - Raise an error when any of the values for --DUR, --PDUR, --ELTM, --STINT, --ENINT, TEDUR, TDSTOFF, TDTGTPAI, TDMINPAI, TDMAXPAI is not ISO 8601 duration.<br>- CORE-002121: Part D - Raise an error when any of the values for --DTC, --STDTC, --ENDTC, --RFTDTC, MIDSDTC, RFSTDTC, RFENDTC, RFXSTDTC, RFXENDTC, RFCSTDTC, RFCENDTC, RFICDTC, RFPENDTC, DTHDTC, BRTHDTC, DMDTC is not ISO 8601 datetime or interval.<br>- CORE-002114: Part E - Raise an error when value for TSVALNF is not populated with a valid ISO 21090 NullFlavor.<br>- CORE-000493: Raise an error when Age Range (AGETXT) is not populated with a number-number format when age range is supplied.<br>For other variable formatting, CG0011 rule identifier is added existing CORE rules as check logic matches exactly.<br>- CORE-002123 (FB1701): Raise an error when CDISC Controlled Terminology specifies the codelist as non-extensible and a term not included in the codelist is used.<br>- CORE-002117 (FB1702): Raise an error when CDISC Controlled Terminology specifies the<br> codelist as extensible and a new term is a duplicate, a synonym or a subset of<br> an existing submission value.<br>Checking adherence to external dictionaries is covered in other CG rules and there CG0011 was not additionally added as authority.<br>- CORE-002120 (CG0400): Raise error when --LOINC is not a valid code in the version of the<br> LOINC dictionary specified in the define.xml document. |
| [CORE-002107](../sdtm_rules/CORE-002107) | Published | Fully Executable | CG0651 | — | — |
| [CORE-002108](../sdtm_rules/CORE-002108) | Published | Partially Executable - Possible Overreporting | CG0155 | — | Explanation: In case of AP split datasets APLB1 or Findings About (APFAMH), this rule will overreport. It will also overreport for AP custom domains. This output should be explained. |
| [CORE-002109](../sdtm_rules/CORE-002109) | Published | Partially Executable - Possible Overreporting | CG0663 | — | Explanation: In case of AP split datasets APLB1 or Findings About (APFAMH), this rule will overreport. It will also overreport for AP custom domains. This output should be explained. |
| [CORE-002110](../sdtm_rules/CORE-002110) | Published | Fully Executable | CG0254 | — | Note: rule was programmed by identifying duplications of IETESTCD values within TI. Multiple occurrences of the same criterion indicate the presence of different criterion versions, in which case TIVERS should be populated to distinguish them. This approach uses duplicated criteria in TI as an indicator of versioning rather than evaluating the study documentation directly.The assumption was made that for new protocol versions, not all criteria are updated at once and thus at least one IETESTCD value will occur more than once. |
| [CORE-002111](../sdtm_rules/CORE-002111) | Published | Fully Executable | CG0336, SEND46, TIG0501 | — | — |
| [CORE-002112](../sdtm_rules/CORE-002112) | Published | Fully Executable | CG0253 | — | Note: rule was programmed by identifying duplications of IETESTCD values within TI. Multiple occurrences of the same criterion indicate the presence of different criterion versions, in which case TIVERS should be populated to distinguish them. This approach uses duplicated criteria in TI as an indicator of versioning rather than evaluating the study documentation directly.The assumption was made that for new protocol versions, not all criteria are updated at once and thus at least one IETESTCD value will occur more than once. |
| [CORE-002113](../sdtm_rules/CORE-002113) | Published | Fully Executable | CG0011 | — | Note: Rule CG0011 specifies: Variable Format = SDTM-specified controlled terminology and format guidelines for variables, when provided. Due to the generic nature of the rule, it was split into 6 parts.<br>- CORE-002106: Part A - Raise an error when value for COUNTRY in DM dataset is not populated with a valid 3-letter country code found in ISO 3166-1.<br>- CORE-002119: Part B - Raise an error when --EVLINT is not ISO 8601 duration or interval.<br>- CORE-002113: Part C - Raise an error when any of the values for --DUR, --PDUR, --ELTM, --STINT, --ENINT, TEDUR, TDSTOFF, TDTGTPAI, TDMINPAI, TDMAXPAI is not ISO 8601 duration.<br>- CORE-002121: Part D - Raise an error when any of the values for --DTC, --STDTC, --ENDTC, --RFTDTC, MIDSDTC, RFSTDTC, RFENDTC, RFXSTDTC, RFXENDTC, RFCSTDTC, RFCENDTC, RFICDTC, RFPENDTC, DTHDTC, BRTHDTC, DMDTC is not ISO 8601 datetime or interval.<br>- CORE-002114: Part E - Raise an error when value for TSVALNF is not populated with a valid ISO 21090 NullFlavor.<br>- CORE-000493: Raise an error when Age Range (AGETXT) is not populated with a number-number format when age range is supplied.<br>For other variable formatting, CG0011 rule identifier is added existing CORE rules as check logic matches exactly.<br>- CORE-XXXXX (FB1701): Raise an error when CDISC Controlled Terminology specifies the codelist as non-extensible and a term not included in the codelist is used.<br>- CORE-002117 (FB1702): Raise an error when CDISC Controlled Terminology specifies the<br> codelist as extensible and a new term is a duplicate, a synonym or a subset of<br> an existing submission value.<br>Checking adherence to external dictionaries is covered in other CG rules and there CG0011 was not additionally added as authority.<br>- CORE-002120 (CG0400): Raise error when --LOINC is not a valid code in the version of the<br> LOINC dictionary specified in the define.xml document. |
| [CORE-002114](../sdtm_rules/CORE-002114) | Published | Fully Executable | CG0011 | — | Note: Rule CG0011 specifies: Variable Format = SDTM-specified controlled terminology and format guidelines for variables, when provided. Due to the generic nature of the rule, it was split into 6 parts.<br>- CORE-002106: Part A - Raise an error when value for COUNTRY in DM dataset is not populated with a valid 3-letter country code found in ISO 3166-1.<br>- CORE-002119: Part B - Raise an error when --EVLINT is not ISO 8601 duration or interval.<br>- CORE-002113: Part C - Raise an error when any of the values for --DUR, --PDUR, --ELTM, --STINT, --ENINT, TEDUR, TDSTOFF, TDTGTPAI, TDMINPAI, TDMAXPAI is not ISO 8601 duration.<br>- CORE-002121: Part D - Raise an error when any of the values for --DTC, --STDTC, --ENDTC, --RFTDTC, MIDSDTC, RFSTDTC, RFENDTC, RFXSTDTC, RFXENDTC, RFCSTDTC, RFCENDTC, RFICDTC, RFPENDTC, DTHDTC, BRTHDTC, DMDTC is not ISO 8601 datetime or interval.<br>- CORE-002114: Part E - Raise an error when value for TSVALNF is not populated with a valid ISO 21090 NullFlavor.<br>- CORE-000493: Raise an error when Age Range (AGETXT) is not populated with a number-number format when age range is supplied.<br>For other variable formatting, CG0011 rule identifier is added existing CORE rules as check logic matches exactly.<br>- CORE-XXXXX (FB1701): Raise an error when CDISC Controlled Terminology specifies the codelist as non-extensible and a term not included in the codelist is used.<br>- CORE-002117 (FB1702): Raise an error when CDISC Controlled Terminology specifies the<br> codelist as extensible and a new term is a duplicate, a synonym or a subset of<br> an existing submission value.<br>Checking adherence to external dictionaries is covered in other CG rules and there CG0011 was not additionally added as authority.<br>- CORE-002120 (CG0400): Raise error when --LOINC is not a valid code in the version of the<br> LOINC dictionary specified in the define.xml document. |
| [CORE-002115](../sdtm_rules/CORE-002115) | Published | Fully Executable | — | FB1113 | — |
| [CORE-002116](../sdtm_rules/CORE-002116) | Published | Fully Executable | — | TRC1735 | — |
| [CORE-002117](../sdtm_rules/CORE-002117) | Published | Fully Executable | CG0011 | FB1702 | Note: Rule CG0011 specifies: Variable Format = SDTM-specified controlled terminology and format guidelines for variables, when provided. Due to the generic nature of the rule, it was split into 6 parts.<br>- CORE-002106: Part A - Raise an error when value for COUNTRY in DM dataset is not populated with a valid 3-letter country code found in ISO 3166-1.<br>- CORE-002119: Part B - Raise an error when --EVLINT is not ISO 8601 duration or interval.<br>- CORE-002113: Part C - Raise an error when any of the values for --DUR, --PDUR, --ELTM, --STINT, --ENINT, TEDUR, TDSTOFF, TDTGTPAI, TDMINPAI, TDMAXPAI is not ISO 8601 duration.<br>- CORE-002121: Part D - Raise an error when any of the values for --DTC, --STDTC, --ENDTC, --RFTDTC, MIDSDTC, RFSTDTC, RFENDTC, RFXSTDTC, RFXENDTC, RFCSTDTC, RFCENDTC, RFICDTC, RFPENDTC, DTHDTC, BRTHDTC, DMDTC is not ISO 8601 datetime or interval.<br>- CORE-002114: Part E - Raise an error when value for TSVALNF is not populated with a valid ISO 21090 NullFlavor.<br>- CORE-000493: Raise an error when Age Range (AGETXT) is not populated with a number-number format when age range is supplied.<br>For other variable formatting, CG0011 rule identifier is added existing CORE rules as check logic matches exactly.<br>- CORE-XXXXX (FB1701): Raise an error when CDISC Controlled Terminology specifies the codelist as non-extensible and a term not included in the codelist is used.<br>- CORE-002117 (FB1702): Raise an error when CDISC Controlled Terminology specifies the<br> codelist as extensible and a new term is a duplicate, a synonym or a subset of<br> an existing submission value.<br>Checking adherence to external dictionaries is covered in other CG rules and there CG0011 was not additionally added as authority.<br>- CORE-002120 (CG0400): Raise error when --LOINC is not a valid code in the version of the<br> LOINC dictionary specified in the define.xml document. |
| [CORE-002118](../sdtm_rules/CORE-002118) | Published | Fully Executable | CG0011 | — | Note: Rule CG0011 specifies: Variable Format = SDTM-specified controlled terminology and format guidelines for variables, when provided. Due to the generic nature of the rule, it was split into 6 parts.<br>- CORE-002106: Part A - Raise an error when value for COUNTRY in DM dataset is not populated with a valid 3-letter country code found in ISO 3166-1.<br>- CORE-002119: Part B - Raise an error when --EVLINT is not ISO 8601 duration or interval.<br>- CORE-002113: Part C - Raise an error when any of the values for --DUR, --PDUR, --ELTM, --STINT, --ENINT, TEDUR, TDSTOFF, TDTGTPAI, TDMINPAI, TDMAXPAI is not ISO 8601 duration.<br>- CORE-002121: Part D - Raise an error when any of the values for --DTC, --STDTC, --ENDTC, --RFTDTC, MIDSDTC, RFSTDTC, RFENDTC, RFXSTDTC, RFXENDTC, RFCSTDTC, RFCENDTC, RFICDTC, RFPENDTC, DTHDTC, BRTHDTC, DMDTC is not ISO 8601 datetime or interval.<br>- CORE-002114: Part E - Raise an error when value for TSVALNF is not populated with a valid ISO 21090 NullFlavor.<br>- CORE-000493: Raise an error when Age Range (AGETXT) is not populated with a number-number format when age range is supplied.<br>For other variable formatting, CG0011 rule identifier is added existing CORE rules as check logic matches exactly.<br>- CORE-XXXXX (FB1701): Raise an error when CDISC Controlled Terminology specifies the codelist as non-extensible and a term not included in the codelist is used.<br>- CORE-002117 (FB1702): Raise an error when CDISC Controlled Terminology specifies the<br> codelist as extensible and a new term is a duplicate, a synonym or a subset of<br> an existing submission value.<br>Checking adherence to external dictionaries is covered in other CG rules and there CG0011 was not additionally added as authority.<br>- CORE-002120 (CG0400): Raise error when --LOINC is not a valid code in the version of the<br> LOINC dictionary specified in the define.xml document. |
| [CORE-002119](../sdtm_rules/CORE-002119) | Published | Fully Executable | CG0011, SEND102 | FB5301 | Note: Rule CG0011 specifies: Variable Format = SDTM-specified controlled terminology and format guidelines for variables, when provided. Due to the generic nature of the rule, it was split into 6 parts.<br>- CORE-002106: Part A - Raise an error when value for COUNTRY in DM dataset is not populated with a valid 3-letter country code found in ISO 3166-1.<br>- CORE-002119: Part B - Raise an error when --EVLINT is not ISO 8601 duration or interval.<br>- CORE-002113: Part C - Raise an error when any of the values for --DUR, --PDUR, --ELTM, --STINT, --ENINT, TEDUR, TDSTOFF, TDTGTPAI, TDMINPAI, TDMAXPAI is not ISO 8601 duration.<br>- CORE-002121: Part D - Raise an error when any of the values for --DTC, --STDTC, --ENDTC, --RFTDTC, MIDSDTC, RFSTDTC, RFENDTC, RFXSTDTC, RFXENDTC, RFCSTDTC, RFCENDTC, RFICDTC, RFPENDTC, DTHDTC, BRTHDTC, DMDTC is not ISO 8601 datetime or interval.<br>- CORE-002114: Part E - Raise an error when value for TSVALNF is not populated with a valid ISO 21090 NullFlavor.<br>- CORE-000493: Raise an error when Age Range (AGETXT) is not populated with a number-number format when age range is supplied.<br>For other variable formatting, CG0011 rule identifier is added existing CORE rules as check logic matches exactly.<br>- CORE-XXXXX (FB1701): Raise an error when CDISC Controlled Terminology specifies the codelist as non-extensible and a term not included in the codelist is used.<br>- CORE-002117 (FB1702): Raise an error when CDISC Controlled Terminology specifies the<br> codelist as extensible and a new term is a duplicate, a synonym or a subset of<br> an existing submission value.<br>Checking adherence to external dictionaries is covered in other CG rules and there CG0011 was not additionally added as authority.<br>- CORE-002120 (CG0400): Raise error when --LOINC is not a valid code in the version of the<br> LOINC dictionary specified in the define.xml document. |
| [CORE-002120](../sdtm_rules/CORE-002120) | Published | Fully Executable | CG0400 | — | — |
| [CORE-002121](../sdtm_rules/CORE-002121) | Published | Fully Executable | CG0011 | — | Note: Rule CG0011 specifies: Variable Format = SDTM-specified controlled terminology and format guidelines for variables, when provided. Due to the generic nature of the rule, it was split into 6 parts.<br>- CORE-002106: Part A - Raise an error when value for COUNTRY in DM dataset is not populated with a valid 3-letter country code found in ISO 3166-1.<br>- CORE-002119: Part B - Raise an error when --EVLINT is not ISO 8601 duration or interval.<br>- CORE-002113: Part C - Raise an error when any of the values for --DUR, --PDUR, --ELTM, --STINT, --ENINT, TEDUR, TDSTOFF, TDTGTPAI, TDMINPAI, TDMAXPAI is not ISO 8601 duration.<br>- CORE-002121: Part D - Raise an error when any of the values for --DTC, --STDTC, --ENDTC, --RFTDTC, MIDSDTC, RFSTDTC, RFENDTC, RFXSTDTC, RFXENDTC, RFCSTDTC, RFCENDTC, RFICDTC, RFPENDTC, DTHDTC, BRTHDTC, DMDTC is not ISO 8601 datetime or interval.<br>- CORE-002114: Part E - Raise an error when value for TSVALNF is not populated with a valid ISO 21090 NullFlavor.<br>- CORE-000493: Raise an error when Age Range (AGETXT) is not populated with a number-number format when age range is supplied.<br>For other variable formatting, CG0011 rule identifier is added existing CORE rules as check logic matches exactly.<br>- CORE-XXXXX (FB1701): Raise an error when CDISC Controlled Terminology specifies the codelist as non-extensible and a term not included in the codelist is used.<br>- CORE-002117 (FB1702): Raise an error when CDISC Controlled Terminology specifies the<br> codelist as extensible and a new term is a duplicate, a synonym or a subset of<br> an existing submission value.<br>Checking adherence to external dictionaries is covered in other CG rules and there CG0011 was not additionally added as authority.<br>- CORE-002120 (CG0400): Raise error when --LOINC is not a valid code in the version of the<br> LOINC dictionary specified in the define.xml document. |
| [CORE-002122](../sdtm_rules/CORE-002122) | Published | Partially Executable - Possible Underreporting | CG0173 | — | Explanation: Condition: Collected data fit a Qualifier variable listed in SDTM: Sections 2.2.1, 2.2.2, or 2.2.3, and are represented in the Findings About domain and rule: The name of the variable is used as the value of FATESTCD.<br>Both condition and rule cannot be programmed directly as selecting the correct FATESTCD requires human review. Instead, the rule is programmed as such: In case value for FATEST matches a variable label with a Qualifier role in the CDISC library, then FATESTCD should be populated with the corresponding variable name of the matching variable label of the CDISC library. Whether or not the collected data fit a qualifier variable is not checked and therefore the rule is listed as partially executable - possible underreporting.<br>The rule will not pick up whether the collected data submitted in FA actually fit the Qualifier role, and it will also not pick up any irrelevant use of 2-character domain codes (e.g. using ECOCCUR instead of OCCUR, AESEV instead of SEV, AETOXGR instead of TOXGR,...). This will need to be checked manually. |
| [CORE-002123](../sdtm_rules/CORE-002123) | Published | Fully Executable | CG0011 | FB1701 | Note: Rule CG0011 specifies: Variable Format = SDTM-specified controlled terminology and format guidelines for variables, when provided. Due to the generic nature of the rule, it was split into 6 parts.<br>- CORE-002106: Part A - Raise an error when value for COUNTRY in DM dataset is not populated with a valid 3-letter country code found in ISO 3166-1.<br>- CORE-002119: Part B - Raise an error when --EVLINT is not ISO 8601 duration or interval.<br>- CORE-002113: Part C - Raise an error when any of the values for --DUR, --PDUR, --ELTM, --STINT, --ENINT, TEDUR, TDSTOFF, TDTGTPAI, TDMINPAI, TDMAXPAI is not ISO 8601 duration.<br>- CORE-002121: Part D - Raise an error when any of the values for --DTC, --STDTC, --ENDTC, --RFTDTC, MIDSDTC, RFSTDTC, RFENDTC, RFXSTDTC, RFXENDTC, RFCSTDTC, RFCENDTC, RFICDTC, RFPENDTC, DTHDTC, BRTHDTC, DMDTC is not ISO 8601 datetime or interval.<br>- CORE-002114: Part E - Raise an error when value for TSVALNF is not populated with a valid ISO 21090 NullFlavor.<br>- CORE-000493: Raise an error when Age Range (AGETXT) is not populated with a number-number format when age range is supplied.<br>For other variable formatting, CG0011 rule identifier is added existing CORE rules as check logic matches exactly.<br>- CORE-XXXXX (FB1701): Raise an error when CDISC Controlled Terminology specifies the codelist as non-extensible and a term not included in the codelist is used.<br>- CORE-002117 (FB1702): Raise an error when CDISC Controlled Terminology specifies the<br> codelist as extensible and a new term is a duplicate, a synonym or a subset of<br> an existing submission value.<br>Checking adherence to external dictionaries is covered in other CG rules and there CG0011 was not additionally added as authority.<br>- CORE-002120 (CG0400): Raise error when --LOINC is not a valid code in the version of the<br> LOINC dictionary specified in the define.xml document. |
| [CORE-002124](../sdtm_rules/CORE-002124) | Published | Fully Executable | CG0659 | — | Note: Rule is split up in 3 rules.<br>- CORE-000031 for QS and FT - Raise an error when --EVAL is present in the QS or FT dataset.<br>- CORE-002124: For RS domain when all RSCAT records in the RS domain have values from the CCCAT code list (Clinical Classification Use case) - Raise an error when RSCAT is only populated with values from the Clinical Classification Use Case as per the define.xml document, but RSEVAL is present in the RS dataset.<br>- CORE-002126: For RS domain some RSCAT records in the RS domain have values from the CCCAT code list (Clinical Classification Use case) but also other codelists are used like for example ONCRSCAT. - Raise an error when some records in the RS dataset have RSCAT populated with values from the Clinical Classification Use Case as per the define.xml document but RSEVAL for those RSCAT records is populated.<br>For the RS domain implementation of the rule some assumptions where made: In case only 1 codelist is used, the codelist will be defined at variable level.In case more than one codelist is used to populate RSCAT, the codelist will be defined at value level. |
| [CORE-002125](../sdtm_rules/CORE-002125) | Published | Fully Executable | CG0660 | — | Note: Rule is split up in 3 rules.<br>- CORE-000032 for QS and FT - Raise an error when --EVALID is present in the QS or FT dataset.<br>- CORE-002125: For RS domain when all RSCAT records in the RS domain have values from the CCCAT code list (Clinical Classification Use case) - Raise an error when RSCAT is only populated with values from the Clinical Classification Use Case as per the define.xml document, but RSEVALID is present in the RS dataset.<br>- CORE-002127: For RS domain some RSCAT records in the RS domain have values from the CCCAT code list (Clinical Classification Use case) but also other codelists are used like for example ONCRSCAT. - Raise an error when some records in the RS dataset have RSCAT populated with values from the Clinical Classification Use Case as per the define.xml document but RSEVALID for those RSCAT records is populated.<br>For the RS domain implementation of the rule some assumptions where made: In case only 1 codelist is used, the codelist will be defined at variable level.In case more than one codelist is used to populate RSCAT, the codelist will be defined at value level. |
| [CORE-002126](../sdtm_rules/CORE-002126) | Published | Fully Executable | CG0659 | — | Note: Rule is split up in 3 rules.<br>- CORE-000031 for QS and FT - Raise an error when --EVAL is present in the QS or FT dataset.<br>- CORE-002124: For RS domain when all RSCAT records in the RS domain have values from the CCCAT code list (Clinical Classification Use case) - Raise an error when RSCAT is only populated with values from the Clinical Classification Use Case as per the define.xml document, but RSEVAL is present in the RS dataset.<br>- CORE-002126: For RS domain some RSCAT records in the RS domain have values from the CCCAT code list (Clinical Classification Use case) but also other codelists are used like for example ONCRSCAT. - Raise an error when some records in the RS dataset have RSCAT populated with values from the Clinical Classification Use Case as per the define.xml document but RSEVAL for those RSCAT records is populated.<br>For the RS domain implementation of the rule some assumptions where made: In case only 1 codelist is used, the codelist will be defined at variable level.In case more than one codelist is used to populate RSCAT, the codelist will be defined at value level. |
| [CORE-002127](../sdtm_rules/CORE-002127) | Published | Fully Executable | CG0660 | — | Note: Rule is split up in 3 rules.<br>- CORE-000032 for QS and FT - Raise an error when --EVALID is present in the QS or FT dataset.<br>- CORE-002125: For RS domain when all RSCAT records in the RS domain have values from the CCCAT code list (Clinical Classification Use case) - Raise an error when RSCAT is only populated with values from the Clinical Classification Use Case as per the define.xml document, but RSEVALID is present in the RS dataset.<br>- CORE-002127: For RS domain some RSCAT records in the RS domain have values from the CCCAT code list (Clinical Classification Use case) but also other codelists are used like for example ONCRSCAT. - Raise an error when some records in the RS dataset have RSCAT populated with values from the Clinical Classification Use Case as per the define.xml document but RSEVALID for those RSCAT records is populated.<br>For the RS domain implementation of the rule some assumptions where made: In case only 1 codelist is used, the codelist will be defined at variable level.In case more than one codelist is used to populate RSCAT, the codelist will be defined at value level. |

## CDISC / FDA IDs implemented by more than one CORE rule

| Organization | Rule ID | CORE ID(s) |
| --- | --- | --- |
| CDISC | CG0011 | [CORE-002106](../sdtm_rules/CORE-002106), [CORE-002113](../sdtm_rules/CORE-002113), [CORE-002114](../sdtm_rules/CORE-002114), [CORE-002117](../sdtm_rules/CORE-002117), [CORE-002118](../sdtm_rules/CORE-002118), [CORE-002119](../sdtm_rules/CORE-002119), [CORE-002121](../sdtm_rules/CORE-002121), [CORE-002123](../sdtm_rules/CORE-002123) |
| CDISC | CG0013 | [CORE-000550](../sdtm_rules/CORE-000550), [CORE-001079](../sdtm_rules/CORE-001079) |
| CDISC | CG0014 | [CORE-000355](../sdtm_rules/CORE-000355), [CORE-000356](../sdtm_rules/CORE-000356) |
| CDISC | CG0336 | [CORE-000272](../sdtm_rules/CORE-000272), [CORE-002111](../sdtm_rules/CORE-002111) |
| CDISC | CG0351 | [CORE-000550](../sdtm_rules/CORE-000550), [CORE-001079](../sdtm_rules/CORE-001079) |
| CDISC | CG0370 | [CORE-000712](../sdtm_rules/CORE-000712), [CORE-000916](../sdtm_rules/CORE-000916), [CORE-000953](../sdtm_rules/CORE-000953) |
| CDISC | CG0372 | [CORE-000220](../sdtm_rules/CORE-000220), [CORE-000541](../sdtm_rules/CORE-000541) |
| CDISC | CG0429 | [CORE-000103](../sdtm_rules/CORE-000103), [CORE-000785](../sdtm_rules/CORE-000785) |
| CDISC | CG0430 | [CORE-000104](../sdtm_rules/CORE-000104), [CORE-000786](../sdtm_rules/CORE-000786) |
| CDISC | CG0531 | [CORE-000844](../sdtm_rules/CORE-000844), [CORE-000845](../sdtm_rules/CORE-000845), [CORE-000846](../sdtm_rules/CORE-000846) |
| CDISC | CG0659 | [CORE-000031](../sdtm_rules/CORE-000031), [CORE-002124](../sdtm_rules/CORE-002124), [CORE-002126](../sdtm_rules/CORE-002126) |
| CDISC | CG0660 | [CORE-000032](../sdtm_rules/CORE-000032), [CORE-002125](../sdtm_rules/CORE-002125), [CORE-002127](../sdtm_rules/CORE-002127) |
| CDISC | SEND12 | [CORE-000355](../sdtm_rules/CORE-000355), [CORE-000356](../sdtm_rules/CORE-000356) |
| CDISC | SEND46 | [CORE-000272](../sdtm_rules/CORE-000272), [CORE-002111](../sdtm_rules/CORE-002111) |
| CDISC | TIG0057 | [CORE-000355](../sdtm_rules/CORE-000355), [CORE-000356](../sdtm_rules/CORE-000356) |
| CDISC | TIG0299 | [CORE-000355](../sdtm_rules/CORE-000355), [CORE-000356](../sdtm_rules/CORE-000356) |
| CDISC | TIG0501 | [CORE-000272](../sdtm_rules/CORE-000272), [CORE-002111](../sdtm_rules/CORE-002111) |
| CDISC | TIG0534 | [CORE-000712](../sdtm_rules/CORE-000712), [CORE-000916](../sdtm_rules/CORE-000916), [CORE-000953](../sdtm_rules/CORE-000953) |
| CDISC | TIG0536 | [CORE-000220](../sdtm_rules/CORE-000220), [CORE-000541](../sdtm_rules/CORE-000541) |
| CDISC | TIG0583 | [CORE-000103](../sdtm_rules/CORE-000103), [CORE-000785](../sdtm_rules/CORE-000785) |
| CDISC | TIG0584 | [CORE-000104](../sdtm_rules/CORE-000104), [CORE-000786](../sdtm_rules/CORE-000786) |
| FDA | FB1115 | [CORE-002063](../sdtm_rules/CORE-002063), [CORE-002064](../sdtm_rules/CORE-002064), [CORE-002065](../sdtm_rules/CORE-002065) |
| FDA | FB1116 | [CORE-000736](../sdtm_rules/CORE-000736), [CORE-002068](../sdtm_rules/CORE-002068), [CORE-002069](../sdtm_rules/CORE-002069), [CORE-002070](../sdtm_rules/CORE-002070) |
