templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '''
                    <div class="front-word">{{Morpheme}}</div>
                    ''',
                    'afmt': '''
                    <div class="front-word">{{Morpheme}}</div>
                    <hr>
                    <div class="section">
                        <strong>English Explanation:</strong> {{EnglishExplanation}}<br>
                        <strong>Chinese Translation:</strong> {{ChineseTranslation}}<br>
                        {{EnglishExplanationAudio}}
                    </div>
                    <div class="section">
                        <strong>Example Words:</strong> {{ExampleWords}}<br>
                        {{ExampleWordsAudio}}
                    </div>
                    <div class="section">
                        <strong>Example Sentence:</strong> {{ExampleSentence}}<br>
                        {{ExampleSentenceAudio}}
                    </div>
                    ''',
                },
            ],
templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '''

                    <div class="front-word" data-anki-audio-field="MorphemeAudio">
                        {{Morpheme}}
                    </div>

                    ''',
                    'afmt': '''


                        <div class="front-word">{{Morpheme}}</div>
                        <hr>
                        <div class="section">
                            <!-- 将 data-audio-source 改为 data-audio-field-name -->
                            <strong data-audio-field-name="EnglishExplanationAudio">English Explanation:</strong> {{EnglishExplanation}}<br>
                            <strong>Chinese Translation:</strong> {{ChineseTranslation}}<br>
                            {{EnglishExplanationAudio}}
                        </div>
                        <div class="section">
                            <strong data-audio-field-name="ExampleWordsAudio">Example Words:</strong> {{ExampleWords}}<br>
                            {{ExampleWordsAudio}}
                        </div>
                        <div class="section">
                            <strong data-audio-field-name="ExampleSentenceAudio">Example Sentence:</strong> {{ExampleSentence}}<br>
                            {{ExampleSentenceAudio}}
                        </div>

                        <!-- !!! 关键改动 !!! -->
                        <!-- 这个 div 专门用来存放 Anki 需要“看见”的音频字段，以便它打包音频。 -->
                        <!-- 由于它被彻底隐藏，Anki 不会为其渲染任何默认播放按钮。 -->
                        <!-- 每个音频字段都被包裹在一个带有唯一ID的span中，便于JavaScript查找。 -->
                        <div id="anki-sound-data" style="display:none; visibility:hidden;">
                            <span id="EnglishExplanationAudio_sound">{{EnglishExplanationAudio}}</span>
                            <span id="ExampleWordsAudio_sound">{{ExampleWordsAudio}}</span>
                            <span id="ExampleSentenceAudio_sound">{{ExampleSentenceAudio}}</span>
                        </div>


                    ''',
                },
            ],


CHAPTER_MORPHEMES_4 = {
    1: [  # Skeletal System
        "oste-o", "crani-o", "cost-o", "spondyl-o", 
        "vertebr-o", "rachi-o", "lumb-o", "ped-o", 
        "pod-o", "dactyl-o", "chir-o"
    ],
    2: [  # Joints & Connective Tissue
        "arthr-o", "chondr-o", "menisc-o", "burs-o",
        "synovi-o", "ligament-o", "tend-o", "tendin-o",
        "fibr-o", "disk-o"
    ],
    3: [  # Bone/Joint Processes & Pathology
        "-blast", "-physis", "-porosis", "-clasia",
        "-clasis", "-clast", "-desis", "-listhesis",
        "-schisis"
    ],
    4: [  # General/Modifying Terms
        "amphi-", "meta-"
    ]
}

CHAPTER_MORPHEMES_4_NEW = {
    1: {
        "chir/o": "",
        "cost/o": "",
        "crani/o": "",
        "dactyl/o": "",
        "lumb/o": "",
        "myel/o": "",
        "oste/o": "",
        "ped/o": "",
        "pod/o": "",
        "rachi/o": "",
        "spondyl/o": "",
        "vertebr/o": ""
    },
    2: {
        "arthr/o": "",
        "burs/o": "",
        "chondr/o": "",
        "disk/o": "",
        "fibr/o": "",
        "ligament/o": "",
        "menisc/o": "",
        "synovi/o": "",
        "ten/o": "",
        "tendin/o": "",
        "tend/o": ""
    },
    3: {
        "-blast": "",
        "-clasia": "",
        "-clasis": "",
        "-clast": "",
        "-desis": "",
        "-listhesis": "",
        "-porosis": "",
        "-physis": "",
        "-shisis": "",
        "-amphi": "",
        "meta-": ""
    },
    4: {
        "-plasty": "",
        "pneum/o": "",
        "-meter": "",
        "cerebr/o": "",
        "abdomin/o": "",
        "-pexy": "",
        "-cyte": "",
        "-tome": "",
        "-centesis": "",
        "-lysis": "",
        "-scope": "",
        "-lith": "",
        "-tomy": "",
        "-sarcoma": "",
        "pleur/o": "",
        "anter/o": "",
        "sym-": "",
        "carp/o": "",
        "tars/o": ""
    }
}

CHAPTER_MORPHEMES_3 = {
    1: {
        'a-': '',
        'an-': '',
        'anti-': '',
        'contra-': '',
        'counter-': '',
        'de-': '',
        'dis-': '',
        'in-': '',
        'im-': '',
        'non-': '',
        'un-': ''
    },
    2: {
        'bi-': '',
        'di-': '',
        'centi-': '',
        'deca-': '',
        'deci-': '',
        'hecto-': '',
        'kilo-': '',
        'milli-': '',
        'mono-': '',
        'uni-': '',
        'hemi-': '',
        'semi-': '',
        'tri-': ''
    },
    3: {
        'ab-': '',
        'ad-': '',
        'circum-': '',
        'dia-': '',
        'epi-': '',
        'extra-': '',
        'inter-': '',
        'intra-': '',
        'per-': '',
        'peri-': '',
        'sub-': '',
        'trans-': ''
    },
    4: {
        '-tic': '',
        'ox/i': '',
        '-emia': '',
        'coagul/o': '',
        '-ception': '',
        'later/o': '',
        'hydr/o': '',
        'somn/i': '',
        'cusp': '',
        '-oxide': '',
        'watt': '',
        'ocul/o': '',
        'nucle/o': '',
        'sphere': '',
        '-plegia': '',
        'lunar': '',
        '-ceps': '',
        '-opia': '',
        '-gon': '',
        'duct': '',
        'articul/o': '',
        'or/o': '',
        'an/o': '',
        'therm/o': '',
        '-lysis': '',
        'dermis': '',
        'cost/o': '',
        'atri/o': '',
        'crani/o': '',
        'nas/o': '',
        'cutane/o': '',
        'oste/o': '',
        'odont/o': '',
        'lingu/o': '',
        'dur/o': '',
        'urethr/o': '',
        'vertebr/o': '',
        'ren/o': '',
        '-rrhea': '',
        'derm/o': ''
    }
}

CHAPTER_MORPHEMES_5 = {
    1: {
        "my-o": "muscle",
        "leiomy-o": "smooth muscle",
        "myocardi-o": "heart muscle",
        "cardiomy-o": "heart muscle",
        "fasci-o": "fascia",
        "sphincter-o": "sphincter",
        "sarc-o": "flesh",
        "rhabd-o": "rod-shaped",
        "myx-o": "mucus",
        "troph-o": "nourishment"
    },
    2: {
        "cephal-o": "head",
        "faci-o": "face",
        "bucc-o": "cheek",
        "gloss-o": "tongue",
        "lingu-o": "tongue",
        "cervic-o": "neck",
        "abdomin-o": "abdomen",
        "inguin-o": "groin",
        "somat-o": "body",
        "axill-o": "armpit",
        "brachi-o": "arm",
        "acr-o": "extremity",
        "-kinesia": "movement",
        "-kinesis": "movement",
        "-plasty": "surgical repair",
        "-rrhaphy": "surgical suture",
        "-meter": "instrument for measuring",
        "-metry": "process of measuring",
        "-spasm": "involuntary contraction",
        "-tonia": "tone, pressure",
        "-lysis": "breaking down",
        "-oid": "resembling",
        "-ceps": "muscular point or head"
    },
    3: {
        "dys-": "bad, difficult or abnormal",
        "eu-": "good, normal",
        "is-o": "equal, same",
        "quadri-": "four",
        "-ad": "toward",
        "femor-o": "femur",
        "poplit-o": "back of the knee",
        "caud-o": "tail",
        "cyst-o": "sac, bladder",
        "hem-o": "blood",
        "hermi-o": "hernia",
        "lip-o": "fat",
        "spher-o": "sphere, ball",
        "phag-o": "eating, swallowing",
        "-scopy": "process of viewing",
        "-plasm": "material forming cells or tissue",
        "-rrhaphy": "surgical suture"
    }
}

CHAPTER_MORPHEMES_TEST = {
    1: {
    "my/o": "",
    "leiomy/o": ""
    },
    2: {
        'append/o': '',
        'sigmoid/o': ''
    },
}

CHAPTER_MORPHEMES_2 = {
    1: {
        "-ation": "",
        "-cian": "",
        "-ia": "",
        "-ism": "",
        "-ist": "",
        "-ity": "",
        "-logy": "",
        "-or": "",
        "-sis": "",
        "-um": ""
    },
    2: {
        "-al": "",
        "-ar": "",
        "-ary": "",
        "-eal": "",
        "-ible": "",
        "-ic": "",
        "-less": "",
        "-ous": ""
    },
    3: {
        "-algia": "",
        "-dynia": "",
        "-cele": "",
        "-itis": "",
        "-megaly": "",
        "-osis": "",
        "-pathy": "",
        "-gram": "",
        "-graph": "",
        "-graphy": ""
    },
    4: {
        "ped/o": "",
        "iatr/o": "",
        "neur/o": "",
        "megal/o": "",
        "cardi/o": "",
        "embol/o": "",
        "dent/i": "",
        "pharmac/o": "",
        "bi/o": "",
        "psych/o": "",
        "erect": "",
        "stern/o": "",
        "cec/o": "",
        "arteri/o": "",
        "muscul/o": "",
        "venul/o": "",
        "bil/i": "",
        "coron/o": "",
        "laryng/o": "",
        "pharyng/o": "",
        "cephal/o": "",
        "ven/o": "",
        "reticul/o": "",
        "trache/o": "",
        "bronchi/o": "",
        "arthr/o": "",
        "my/o": "",
        "encephal/o": "",
        "enter/o": "",
        "hepat/o": "",
        "splen/o": "",
        "aden/o": "",
        "angi/o": "",
        "electr/o": "",
        "radi/o": "",
        "gynec/o": "",
        "acr/o": "",
        "cholecyst/o": "",
        "steth/o": "",
        "ur/o": "",
        "omphal/o": ""
    }
}

CHAPTER_MORPHEMES_6 = {
    1: {
        'aden/o': '',
        'cheil/o': '',
        'labi/o': '',
        'dent/i': '',
        'odont/o': '',
        'duoden/o': '',
        'enter/o': '',
        'esophag/o': '',
        'gastr/o': '',
        'ile/o': '',
        'jejun/o': '',
        'or/o': '',
        'stomat/o': ''
    },
    2: {
        'append/o': '',
        'appendic/o': '',
        'cec/o': '',
        'chol/e': '',
        'cholangi/o': '',
        'cholecyst/o': '',
        'choledoch/o': '',
        'col/o': '',
        'colon/o': '',
        'hepat/o': '',
        'pancreat/o': '',
        'proct/o': '',
        'rect/o': '',
        'sigmoid/o': ''
    },
    3: {
        'amyl/o': '',
        'glyc/o': '',
        'gluc/o': '',
        'lip/o': '',
        'phag/o': '',
        '-ase': '',
        '-ectomy': '',
        '-orexia': '',
        '-pepsia': '',
        '-pexy': '',
        '-stomy': '',
        '-tomy': ''
    },
    4: {
        '-schisis': '',
        '-cle': '',
        'orth/o': '',
        '-ptosis': '',
        '-emesis': '',
        '-stasis': '',
        '-lithiasis': '',
        '-penia': '',
        'eu-': '',
        'nephr/o': ''
    }
}

CHAPTER_MORPHEMES_7 = {
    1: {
        "angi/o": "",
        "aort/o": "",
        "arteri/o": "",
        "arteriol/o": "",
        "atri/o": "",
        "cardi/o": "",
        "pericardi/o": "",
        "phleb/o": "",
        "ven/o": "",
        "sept/o": "",
        "valvul/o": "",
        "ventricul/o": "",
        "venul/o": ""
    },
    2: {
        "cyt/o": "",
        "electr/o": "",
        "erythr/o": "",
        "granul/o": "",
        "hem/o": "",
        "hemat/o": "",
        "kary/o": "",
        "nucle/o": "",
        "leuk/o": "",
        "morph/o": "",
        "sider/o": "",
        "sphygm/o": "",
        "thromb/o": ""
    },
    3: {
        "-cytosis": "",
        "-emia": "",
        "-malacia": "",
        "-penia": "",
        "-phil": "",
        "-rrhage": "",
        "-rrhagia": "",
        "-sclerosis": "",
        "-stasis": "",
        "brady-": "",
        "tachy-": ""
    },
    4: {
        "-sclerosis": "",
        "-malacia": "",
        "-oma": "",
        "-cide": "",
        "-cyte": "",
        "-globin": "",
        "mega-": "",
        "-lytic": "",
        "-roid": "",
        "-blast": "",
        "-clast": "",
        "-lysis": "",
        "bas/o": ""
    }
}

CHAPTER_MORPHEMES_8 = {
    1: {
        "alveol/o": "",
        "bronch/o": "",
        "bronchi/o": "",
        "bronchiol/o": "",
        "epiglott/o": "",
        "laryng/o": "",
        "mediastin/o": "",
        "palat/o": "",
        "pharyng/o": "",
        "rhin/o": "",
        "trache/o": ""
    },
    2: {
        "atel/o": "",
        "coni/o": "",
        "lob/o": "",
        "orth/o": "",
        "ox/i": "",
        "phren/o": "",
        "pneumon/o": "",
        "pneum/o": "",
        "pulmon/o": "",
        "py/o": "",
        "spir/o": "",
        "thorac/o": ""
    },
    3: {
        "-capnia": "",
        "-ectasis": "",
        "-ectasia": "",
        "-form": "",
        "-oxia": "",
        "-phonia": "",
        "-pnea": "",
        "-ptysis": "",
        "-stenosis": "",
        "-thorax": "",
        "brachy-": ""
    },
    4: {
        "-edema": "",
        "cruc/i": "",
        "dendr/i": "",
        "melan/o": "",
        "hydr/o": ""
    }
}

CHAPTER_MORPHEMES_9 = {
    1: {
        "astr/o": "",
        "cortic/o": "",
        "gangli/o": "",
        "ganglion/o": "",
        "gli/o": "",
        "medull/o": "",
        "mnes/o": "",
        "myel/o": "",
        "neur/o": "",
        "psych/o": "",
        "radicul/o": "",
        "schiz/o": ""
    },
    2: {
        "cerebell/o": "",
        "cerebr/o": "",
        "dur/o": "",
        "encephala/o": "",
        "lept/o": "",
        "mening/o": "",
        "poli/o": "",
        "pont/o": "",
        "thalam/o": ""
    },
    3: {
        "-asthenia": "",
        "-esthesia": "",
        "-in": "",
        "-lemma": "",
        "-lexia": "",
        "-mania": "",
        "-paresis": "",
        "-phasia": "",
        "-phobia": "",
        "-phrenia": "",
        "-plegia": "",
        "-taxia": ""
    },
    4: {
        "-tropic": "",
        "-plegic": "",
        "-plasia": "",
        "gyr/o": "",
        "prosop/o": "",
        "arachn/o": "",
        "pyr/o": "",
        "gynec/o": "",
        "hebe-": "",
        "cry/o": "",
        "klept/o": "",
        "para-": ""
    }
}