# Conditional life-aspect engine contract

The explicit birth entry point and existing calculate adapter now return
`life_aspect_candidates`. This is source-linked traditional conditional reading
content, not a selected personalized forecast or evidence of predictive accuracy.
Source: https://archive.org/details/in.ernet.dli.2015.92117
Original PDF79-83 pixels inspected, PhaladeepikaIV.23, V.1-9.

## Career

`career.candidates` always has Lagna, Moon and Sun alternatives, in that order.
Each has a whole-sign tenth sign/lord, the tenth lord's actual Navamsa sign/owner,
source metadata, historical livelihood examples, and `conditional_reading`.
`selected_reference` and `selected_profession` are null. Same owners across two
routes do not prove selection or independently corroborate the prediction.
The strongest-reference comparison and degree-bhava application remain unset.

Example, synthetic birth2000-01-01 at14:30 Asia/Kolkata,13N/80E:

- Lagna: tenth lordSaturn, Navamsa ownerSun. If this route is strongest, the
  source links livelihood to fruit trees, wool, medicine, metals, ritual work,
  or service under a ruler or respected person.
- Moon: tenth lordMoon, Navamsa ownerJupiter. If this route is strongest, the
  source links livelihood to religious instruction, scriptural study,
  patronage, or money lending.
- Sun: tenth lordMercury, Navamsa ownerMercury. If this route is strongest, the
  source links livelihood to writing, poetry, clerical work, scriptural study,
  astrology, or priestly work.

Do not silently turn these into a single job, reinterpret Mercury as software
engineering, Sun as government employment, Saturn as an engineering guarantee,
or treat the listed alternatives as things the person should do.

## Wealth, marriage, health and timing

Each career candidate also includes a sourceV.9 `wealth_conditional_reading`:
strong Navamsa owner is associated with easier acquisition, weak with little
wealth. Its strength is null, not inferred from one dignity flag. The wealth
section's `selected_outcome` remains null. No income amount, financial advice,
foreign move, current-period label, event date, marriage outcome, medical
prediction, lifespan or death claim is provided. The latter sections have null
readings and explicit statuses, not placeholder advice.

## Presentation requirements

Show alternatives as alternatives with their conditions adjacent. Preserve the
selection and strength caveats with the prose, not just in a raw report hidden
behind a disclosure. All examples are selected non-stigmatizing subsets, not
exhaustive verse translations. Do not infer person's gender from historical
wording. Do not claim a complete life reading, Balaji method match, predictive
accuracy, source strength selection, or validated fate. This slice adds genuine
source-based interpretation content but does not solve the requested full
personal prediction layer. The shell is a separate owner-controlled change.

## Marriage conditional readings

`engine/marriage_conditional.py` evaluates the scan-checked Phaladeepika (Adh. VIII, X) and Brihat Jataka conditions on whole-sign Lagna geometry. Each rule returns met / possibly_met / not_met / unresolved with source pages, an own-words effect and what it needs. "Benefic" is undefined in the sentences, so Jupiter and Venus count as definite and Mercury and the Moon only as possible. Strength-conditioned rules take the Shadbala working-profile verdicts. Rules whose effect is an adverse marital-status text (Sun in the 7th, Moon with Saturn in the 7th, and similar) carry `ship_default: false`. Spouse-death, body, character and "wicked spouse" wording is held out. The Moon-with-Saturn rule needs the native's sex because the books differ by chart type. No timing is selected: the period-candidate row lists the lords only.

## Wealth conditional readings

`engine/wealth_conditional.py` evaluates the scan-checked Phaladeepika VI (Sunapha/Anapha/Durudhara, Subhakartari, Vasumat, Amala, Adhiyoga, sign-exchange yogas, Maha yoga) and VIII (planets in the 2nd and 11th, wealth clause only) conditions. Same status vocabulary as marriage. Held out: Kemadruma and its cancellation, Srikantha/Srinatha/Virinchi/Parvata (conditions not transcribed in the research file), bad-yoga wording, node placements. No income amount or level is produced. Placement rows carry the planet's Shadbala verdict, and note that VIII.34-35 (position within the bhava) and XV (house strength) scale the effect and are not computed.
