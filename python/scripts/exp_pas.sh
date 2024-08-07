#!/bin/bash

# 定义数组
pre20163=("param0=(0.6754015968235019 0.6973980378869656 0.6594262862515415)" 
"param0=(1 1 1)" 
"param0=(1 1 1)" 
"param0=(1 1 1)" 
"param0=(1 1 1)")

post20163=("param00=(0.04978706836786395 0.1353352832366127 0.36787944117144233)" 
"param00=(0.1091004960023879 0.22873628180526534 0.46849265117713607)"
"param00=(0.3303036421270403 0.4782638202971926 0.6844652300717226)"
"param00=(0.4778323788043405 0.6115683745549377 0.7766659417755923)"
"param00=(0.5747204904360382 0.6915662081805274 0.8273241384558548)")

pre20193=("param0=(0.3400293208877289 0.34649084963007704 0.36162086665407117)"
"param0=(0.6800586417754578 0.6929816992601541 0.7232417333081423)"
"param0=(1 1 1)"
"param0=(1 1 1)"
"param0=(1 1 1)")

post20193=("param00=(0.04978706836786395 0.1353352832366127 0.36787944117144233)"
"param00=(0.04978706836786395 0.1353352832366127 0.36787944117144233)"
"param00=(0.11670775664146053 0.24344808499414872 0.5009085211374322)"
"param00=(0.23881768312682666 0.38988594097684204 0.6307234039702508)"
"param00=(0.3416251698008514 0.49340458550174493 0.7077489110817707)")

pre20167=("param0=(1 0.9374369185347935 1 1 1 1 1)"
"param0=(1 1 1 1 1 1 1)"
"param0=(1 1 1 1 1 1 1)"
"param0=(1 1 1 1 1 1 1)"
"param0=(1 1 1 1 1 1 1)")

post20167=("param00=(0.001388216704270359 0.0034961073419394104 0.009503405057936154 0.024794993570595083 0.0643924968608941 0.1615352660519124 0.3936464605261223)"
"param00=(0.03603599881283172 0.05718739449668012 0.09748540946180691 0.15746426124868806 0.25375676712335005 0.4019145009226619 0.627412512248618)"
"param00=(0.1898320786740504 0.23913948675702423 0.3122272009657807 0.396818339087659 0.5037433913467927 0.6339678002337213 0.7920940902291207)"
"param00=(0.3303036421270403 0.38527229627285225 0.46023611624759475 0.5400011109931291 0.6331010429010641 0.737980490310301 0.8560869757810124)"
"param00=(0.43569723280513317 0.48901890224921185 0.5587729422276823 0.6299351864181417 0.7097488227160315 0.7962209493813394 0.8899966798978076)")

pre20197=("param0=(0.811276694356305 0.5793323800350486 0.6179613561991663 0.44248300984246225 0.374395353683818 0.674973674973675 0.526575004338855)"
"param0=(1 1 1 0.8849660196849245 0.748790707367636 1 1)"
"param0=(1 1 1 1 1 1 1)"
"param0=(1 1 1 1 1 1 1)"
"param0=(1 1 1 1 1 1 1)")

post20197=("param00=(0.0009118819655545166 0.0024787521766663594 0.006737946999085469 0.018315638888734186 0.04978706836786395 0.1353352832366127 0.36787944117144233)"
"param00=(0.0025318905287762053 0.0046892788536723904 0.011115507639160489 0.024964462178638132 0.06786044389744514 0.1844638115175896 0.3869219261609263)"
"param00=(0.039870228769679786 0.05425990763315014 0.08353920308331102 0.12519484958411123 0.22027212869744037 0.429493169259816 0.6220310272663637)"
"param00=(0.11670775664146053 0.1433243172752553 0.19109998693681718 0.2502599435894261 0.3647315228090452 0.5692516831897996 0.7286877175300125)"
"param00=(0.1996753083625509 0.2329375616622406 0.2890314915079515 0.35382884221627725 0.46933157649729934 0.6553572836703778 0.788689436512474)")

mems=(50 100 200 300 400)
prior=(3 7)
dataset=(2016 2019)
highs=("H=(3)" "H=(6 7)")
lows=("L=(1 2)" "L=(1 2 3 4 5)")

for _prior in "${prior[@]}"
do
    high_array=("${highs[@]}")
    low_array=("${lows[@]}")
    if [ $_prior -eq 3 ] ; then
        param_high="${high_array[0]}"
        param_low="${low_array[0]}"
    elif [ $_prior -eq 7 ] ; then
        param_high="${high_array[1]}"
        param_low="${low_array[1]}"
    fi
    eval $param_high
    eval $param_low
    for _dataset in "${dataset[@]}"
    do
        for i in $(seq 0 4) 
        do
            if [ "${_dataset}" -eq 2016 ] ; then
                #echo "PAS(${_dataset},${_prior},mem=${mems[$i]}) is running..."
                if [ "${_prior}" -eq 3 ] ; then
                    pre_array=("${pre20163[@]}")
                    post_array=("${post20163[@]}")
                elif [ "${_prior}" -eq 7 ] ; then
                    pre_array=("${pre20167[@]}")
                    post_array=("${post20167[@]}")
                fi
            else
                #echo "PAS(${_dataset},${_prior},mem=${mems[$i]}) is running..."
                if [ "${_prior}" -eq 3 ] ; then
                    pre_array=("${pre20193[@]}")
                    post_array=("${post20193[@]}")
                elif [ "${_prior}" -eq 7 ] ; then
                    pre_array=("${pre20197[@]}")
                    post_array=("${post20197[@]}")
                fi
            fi

            param_pre="${pre_array[$i]}"
            param_post="${post_array[$i]}"
            eval $param_pre
            eval $param_post
            if [ "${_prior}" -eq 3 ] ; then
                #echo "PAS(${_dataset},${_prior},mem=${mems[$i]},pre = ${param0[0]} ${param0[1]} ${param0[2]}, post= ${param00[0]} ${param00[1]} ${param00[2]}) is running..."
                python -W ignore ../main.py --method "pas" --dataset "${_dataset}" --prior_num "${_prior}" --mem_kb "${mems[$i]}" --pre ${param0[0]} ${param0[1]} ${param0[2]} --post ${param00[0]} ${param00[1]} ${param00[2]} --high_prior ${H[0]} --low_prior ${L[0]} ${L[1]}
            elif [ "${_prior}" -eq 7 ] ; then
                #echo "PAS(${_dataset},${_prior},mem=${mems[$i]},pre = ${param0[0]} ${param0[1]} ${param0[2]} ${param0[3]} ${param0[4]} ${param0[5]}, ${param0[6]}, post= ${param00[0]} ${param00[1]} ${param00[2]} ${param00[3]} ${param00[4]} ${param00[5]} ${param00[6]}) is running..."
                python -W ignore ../main.py --method "pas" --dataset "${_dataset}" --prior_num "${_prior}" --mem_kb "${mems[$i]}" --pre ${param0[0]} ${param0[1]} ${param0[2]} ${param0[3]} ${param0[4]} ${param0[5]} ${param0[6]} --post ${param00[0]} ${param00[1]} ${param00[2]} ${param00[3]} ${param00[4]} ${param00[5]} ${param00[6]} --high_prior ${H[0]} ${H[1]} --low_prior ${L[0]} ${L[1]} ${L[2]} ${L[3]} ${L[4]}
            fi
            
            
        done
    done
done