# Chapter 3 header and the argument ladder. Italian quotes are copied from ~/.atlas-cache/src/machiavelli/1-2.txt.
# Shalem Hebrew we have for this chapter: the "venom" line (p. 14) and the "new order" line (p. 15). Pages follow the
# atlas specification (story A p. 14, story B p. 15); lines between them are marked 14-15.
H = {'n':3, 'eyebrow':'ספר ראשון, פרק 3 · עמ׳ 14–15', 'title':'אילו אירועים הביאו ליצירת הטריבונים',
 'full':'"אילו מקרים גרמו ליצירת טריבוני הפלבס ברומא, מה שעשה את הרפובליקה מושלמת יותר" (תרגום חופשי)',
 'oneline':'מי שמסדר רפובליקה צריך להניח שכל בני האדם רעים. ברומא זה נראה רק כשמתו הטרקווינים: הפחד נעלם, האצילים פגעו בפלבס, ומתוך המהומות נולדו הטריבונים.',
 'intro':'שני סיפורים מהפרק, שבאים זה אחרי זה. בחרו סיפור כדי ללכת בו צעד אחר צעד.',
 'question':'מקיאוולי טוען שהאצילים נהגו יפה רק כי פחדו מהמלך. ואם כך, מה בדיוק עושים הטריבונים: מחליפים את הפחד, או מחליפים את המלך? ומה זה אומר על אנשים שמתנהגים יפה רק כשמישהו מסתכל?',
 'next':'ממשיך בפרק 4: הפירוד בין הפלבס לסנאט עשה את רומא חופשית ועצומה.',
 'overviewBounds':[[40.7,11.6],[43.1,14.2]], 'hideOther':True}
LADDER = [
 {'role':['העיקרון','rule'], 'pg':'עמ׳ 14', 'h':'להניח שכולם רעים', 'q':'"è necessario a chi dispone una republica, ed ordina leggi in quella, presupporre tutti gli uomini rei": מי שמסדר רפובליקה ומחוקק בה חוקים צריך להניח שכל בני האדם רעים', 'tr':True, 'at':[0,0]},
 {'role':['המראה',''], 'pg':'עמ׳ 14', 'h':'איחוד גדול מאוד', 'q':'"Pareva che fusse in Roma intra la Plebe ed il Senato, cacciati i Tarquini, una unione grandissima": נראה היה שאחרי שגורשו הטרקווינים שרר ברומא איחוד גדול מאוד בין הפלבס לסנאט', 'tr':True, 'at':[0,0]},
 {'role':['הסיבה הנסתרת','evid'], 'pg':'עמ׳ 14', 'h':'הפחד מהמלך', 'q':'"dei quali temendo la Nobilità, ed avendo paura che la Plebe male trattata non si accostasse loro, si portava umanamente con quella": האצולה פחדה מהם, וחששה שהפלבס יתקרב אליהם, ולכן נהגה בו באנושיות', 'tr':True, 'at':[0,1]},
 {'role':['המפנה','evid'], 'pg':'עמ׳ 14', 'h':'הרעל', 'q':'ברגע שמתו הטארקווינים ופחדם של האצילים נעלם, הם החלו לירוק על פשוטי העם את אותו רעל ששמרו בחזם', 'at':[0,4]},
 {'role':['הכלל','rule'], 'pg':'עמ׳ 14–15', 'h':'רק מתוך כורח', 'q':'"gli uomini non operono mai nulla bene, se non per necessità": בני האדם לא עושים שום דבר טוב אלא מתוך כורח', 'tr':True, 'at':[1,0]},
 {'role':['הניגוד','cave'], 'pg':'גיצ׳ארדיני', 'h':'מוחלט מדי', 'q':'"È posto troppo assolutamente che gli uomini non operano mai bene se non per necessitá": נאמר באופן מוחלט מדי שבני האדם לעולם אינם עושים טוב אלא מתוך כורח', 'tr':True},
 {'role':['הכלל','rule'], 'pg':'עמ׳ 14–15', 'h':'הרעב, העוני והחוקים', 'q':'"la fame e la povertà fa gli uomini industriosi, e le leggi gli fanno buoni": הרעב והעוני עושים את בני האדם חרוצים, והחוקים עושים אותם טובים', 'tr':True, 'at':[1,1]},
 {'role':['הפתרון','rule'], 'pg':'עמ׳ 15', 'h':'סדר חדש במקום הפחד', 'q':'סדר חדש שתהיה לו אותה השפעה שהייתה לטארקווינים', 'at':[1,3]},
 {'role':['הסיום',''], 'pg':'עמ׳ 15', 'h':'מתווכים בין הפלבס לסנאט', 'q':'"che poterono essere sempre di poi mezzi intra la Plebe e il Senato, e ovviare alla insolenzia de\' Nobili": שיכלו מאז ותמיד להיות מתווכים בין הפלבס לסנאט, ולמנוע את חוצפת האצילים', 'tr':True, 'at':[1,4]},
]
