# Chapter 4 header and the argument ladder. Italian quotes are copied from ~/.atlas-cache/src/machiavelli/1-2.txt.
# Shalem Hebrew we have for this chapter (as quoted in the project's summaries of chapters 17 and 13): the "first cause"
# line (p. 15) and "laws and orders" (p. 16). Pages follow the atlas specification (pp. 15-17); a line between two known
# pages is marked with both.
H = {'n':4, 'eyebrow':'ספר ראשון, פרק 4 · עמ׳ 15–17', 'title':'הפירוד עשה את הרפובליקה חופשית',
 'full':'"שהפירוד בין הפלבס לסנאט הרומי עשה את הרפובליקה ההיא חופשית ועצומה" (תרגום חופשי)',
 'oneline':'מי שמגנה את המהומות ברומא מגנה את מה ששמר עליה חופשית. במשך יותר משלוש מאות שנה, עד הגרכים, הן הולידו מעט גלות, מעט מאוד דם, והרבה חוקים.',
 'intro':'שלושה סיפורים מהפרק. בחרו סיפור כדי ללכת בו צעד אחר צעד.',
 'question':'מקיאוולי אומר שהמהומות ברומא כמעט לא שפכו דם, ולכן היו טובות. ומה עם הגרכים, שבהם נגמרה הספירה? האם הם ההוכחה שהוא צודק, כי עד אז זה עבד, או ההוכחה שהוא טועה, כי ככה זה נגמר?',
 'next':'ממשיך בפרק 5: בידי מי בטוח יותר להפקיד את השמירה על החירות, בידי העם או בידי הגדולים.',
 'overviewBounds':[[41.872,12.452],[41.948,12.552]], 'hideOther':True}
LADDER = [
 {'role':['הטענה שכנגד','cave'], 'pg':'עמ׳ 15', 'h':'רפובליקה של מהומות', 'q':'"Roma essere stata una republica tumultuaria, e piena di tanta confusione che, se la buona fortuna e la virtù militare non avesse sopperito a\' loro difetti, sarebbe stata inferiore a ogni altra republica": שרומא הייתה רפובליקה של מהומות ומלאה בלבול כל כך, שאלמלא הפורטונה הטובה והמידה הטובה הצבאית היו משלימות את פגמיה, הייתה נחותה מכל רפובליקה אחרת', 'tr':True, 'at':[2,4]},
 {'role':['התשובה','rule'], 'pg':'עמ׳ 15', 'h':'מי שמגנה את המהומות', 'q':'אותם דברים שהיו הסיבה הראשית לכך שרומא נשמרה חופשייה', 'at':[0,1]},
 {'role':['הכלל','rule'], 'pg':'עמ׳ 15–16', 'h':'שני מצבי רוח', 'q':'"come e\' sono in ogni republica due umori diversi, quello del popolo, e quello de\' grandi; e come tutte le leggi che si fanno in favore della libertà, nascano dalla disunione loro": שבכל רפובליקה יש שני מצבי רוח שונים, של העם ושל הגדולים, ושכל החוקים שנעשים לטובת החירות נולדים מהפירוד ביניהם', 'tr':True, 'at':[2,0]},
 {'role':['הראיה','evid'], 'pg':'עמ׳ 15–16', 'h':'שלוש מאות שנה', 'q':'"non mandò in esilio più che otto o dieci cittadini, e ne ammazzò pochissimi, e non molti ancora ne condannò in danari": לא שלחה לגלות יותר משמונה או עשרה אזרחים, הרגה מעטים מאוד, וגם לא רבים קנסה בכסף', 'tr':True, 'at':[1,4]},
 {'role':['השרשרת','rule'], 'pg':'עמ׳ 15–16', 'h':'מהמהומות לדוגמאות', 'q':'"li buoni esempli nascano dalla buona educazione, la buona educazione, dalle buone leggi; e le buone leggi, da quelli tumulti": הדוגמאות הטובות נולדות מחינוך טוב, החינוך הטוב מחוקים טובים, והחוקים הטובים מאותן מהומות', 'tr':True, 'at':[2,2]},
 {'role':['התוצאה','rule'], 'pg':'עמ׳ 16', 'h':'לא גלות ולא אלימות', 'q':'חוקים וסדרים לטובת החירות הציבורית', 'at':[0,5]},
 {'role':['הדרכים','evid'], 'pg':'עמ׳ 16–17', 'h':'לצעוק, לצאת, לא להתגייס', 'q':'"partirsi tutta la plebe di Roma ... o e\' non voleva dare il nome per andare alla guerra": שכל הפלבס של רומא יוצא ממנה... או שלא רצה למסור את שמו כדי לצאת למלחמה', 'tr':True, 'at':[0,2]},
 {'role':['מקור הרצונות','rule'], 'pg':'עמ׳ 16–17', 'h':'מדיכוי, או מחשד', 'q':'"e\' nascono, o da essere oppressi, o da suspizione di avere ad essere oppressi": הם נולדים או מכך שמדכאים אותם, או מהחשד שידכאו אותם', 'tr':True, 'at':[2,3]},
 {'role':['התרופה','rule'], 'pg':'עמ׳ 16–17', 'h':'אדם שראוי לאמון', 'q':'"li popoli, come dice Tullio, benché siano ignoranti, sono capaci della verità": העמים, כמו שאומר טוליוס, אף שהם בורים, מסוגלים לקבל את האמת', 'tr':True, 'at':[0,4]},
 {'role':['הניגוד','cave'], 'pg':'גיצ\'ארדיני', 'h':'לשבח את המחלה', 'q':'"ma laudare le disunione è come laudare in uno infermo la infermitá, per la bontá del remedio che gli è stato applicato": אבל לשבח את הפירוד זה כמו לשבח אצל חולה את המחלה, בגלל הטיב של התרופה שניתנה לו', 'tr':True},
 {'role':['הסיום',''], 'pg':'עמ׳ 16–17', 'h':'ראויות לשבח עליון', 'q':'"E se i tumulti furano cagione della creazione de\' Tribuni, meritano somma laude": ואם המהומות היו הסיבה ליצירת הטריבונים, הן ראויות לשבח עליון', 'tr':True, 'at':[0,1]},
]
