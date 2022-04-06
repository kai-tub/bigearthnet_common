Search.setIndex({docnames:["00_constants","05_base","10_sets","api","api_base","api_constant","api_sets","intro"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":5,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.intersphinx":1,sphinx:56},filenames:["00_constants.ipynb","05_base.md","10_sets.md","api.md","api_base.md","api_constant.md","api_sets.md","intro.md"],objects:{"bigearthnet_common.base":[[4,1,1,"","Resource"],[4,2,1,"","ben_19_labels_to_multi_hot"],[4,2,1,"","ben_43_labels_to_multi_hot"],[4,2,1,"","get_complete_s1_to_s2_patch_name_mapping"],[4,2,1,"","get_complete_s2_to_s1_patch_name_mapping"],[4,2,1,"","get_original_split_from_patch_name"],[4,2,1,"","get_patches_to_country_mapping"],[4,2,1,"","get_patches_to_season_mapping"],[4,2,1,"","get_s1_patch_directories"],[4,2,1,"","get_s1_patches_from_original_test_split"],[4,2,1,"","get_s1_patches_from_original_train_split"],[4,2,1,"","get_s1_patches_from_original_validation_split"],[4,2,1,"","get_s1_patches_with_cloud_and_shadow"],[4,2,1,"","get_s1_patches_with_no_19_class_target"],[4,2,1,"","get_s1_patches_with_seasonal_snow"],[4,2,1,"","get_s2_patch_directories"],[4,2,1,"","get_s2_patches_from_original_test_split"],[4,2,1,"","get_s2_patches_from_original_train_split"],[4,2,1,"","get_s2_patches_from_original_validation_split"],[4,2,1,"","get_s2_patches_with_cloud_and_shadow"],[4,2,1,"","get_s2_patches_with_no_19_class_target"],[4,2,1,"","get_s2_patches_with_seasonal_snow"],[4,2,1,"","is_cloudy_shadowy_patch"],[4,2,1,"","is_snowy_patch"],[4,2,1,"","old2new_labels"],[4,2,1,"","parse_datetime"],[4,2,1,"","read_S1_json"],[4,2,1,"","read_S2_json"],[4,2,1,"","s1_to_s2_patch_name"],[4,2,1,"","s2_to_s1_patch_name"],[4,2,1,"","validate_ben_s1_root_directory"],[4,2,1,"","validate_ben_s2_root_directory"]],"bigearthnet_common.constants":[[5,1,1,"","Country"],[5,1,1,"","Season"],[5,1,1,"","SentinelSource"],[5,1,1,"","Split"],[5,2,1,"","cli"],[5,2,1,"","print_all_constants"],[5,2,1,"","smart_pprint"]],"bigearthnet_common.constants.Country":[[5,3,1,"","Austria"],[5,3,1,"","Belgium"],[5,3,1,"","Finland"],[5,3,1,"","Ireland"],[5,3,1,"","Kosovo"],[5,3,1,"","Lithuania"],[5,3,1,"","Luxembourg"],[5,3,1,"","Portugal"],[5,3,1,"","Serbia"],[5,3,1,"","Switzerland"],[5,4,1,"","to_iso_A2"]],"bigearthnet_common.constants.Season":[[5,3,1,"","Fall"],[5,3,1,"","Spring"],[5,3,1,"","Summer"],[5,3,1,"","Winter"]],"bigearthnet_common.constants.SentinelSource":[[5,3,1,"","S1"],[5,3,1,"","S2"]],"bigearthnet_common.constants.Split":[[5,3,1,"","test"],[5,3,1,"","train"],[5,3,1,"","validation"]],"bigearthnet_common.sets":[[6,2,1,"","build_csv_sets"],[6,2,1,"","build_set"],[6,2,1,"","filter_patches_by_country"],[6,2,1,"","filter_patches_by_season"],[6,2,1,"","filter_patches_by_split"],[6,2,1,"","get_all_s1_patches"],[6,2,1,"","get_all_s2_patches"]],bigearthnet_common:[[4,0,0,"-","base"],[5,0,0,"-","constants"],[6,0,0,"-","sets"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","function","Python function"],"3":["py","attribute","Python attribute"],"4":["py","method","Python method"]},objtypes:{"0":"py:module","1":"py:class","2":"py:function","3":"py:attribute","4":"py:method"},terms:{"0":[0,4],"005199781653162433":0,"006560509961089494":0,"008465897454337377":0,"008734514272831312":0,"008894170396581979":0,"009006419425650416":0,"009372347973754483":0,"010313381699397267":0,"011137533780880447":0,"012495116691081101":0,"014506503161364157":0,"01480586":0,"015401347239032578":0,"016467393967040514":0,"01672411392172122":0,"01943166141573205":0,"019872271123826963":0,"02069333781261921":0,"02083552146242466":0,"024329395724727244":0,"02735123071168078":0,"03166961092378119":0,"033858938487067974":0,"03427268705882353":0,"03458396840024414":0,"0605464":0,"1":[0,4,6],"10":0,"1009":0,"1079":0,"1096":0,"11":0,"111":0,"112":0,"12":0,"1200":0,"121":0,"122":0,"123":0,"124":0,"1273":0,"13":0,"1302":0,"131":0,"132":0,"133":0,"1356":0,"1365":0,"13789355":0,"14":0,"141":0,"142":0,"15":0,"1594":0,"16":0,"17":0,"1792":0,"18":0,"19":[0,1,4,7],"19066363":0,"2":[0,2,4,6,7],"20":0,"2075":0,"21":0,"211":0,"212":0,"213":0,"21682446":0,"22":0,"221":0,"2218":0,"222":0,"223":0,"2246":0,"2266":0,"23":0,"231":0,"23569706":0,"24":0,"241":0,"242":0,"243":0,"244":0,"25":0,"255":0,"26":0,"27":0,"28":0,"29":0,"3":0,"30":0,"31":0,"311":0,"312":0,"313":0,"32":0,"321":0,"322":0,"323":0,"324":0,"32729131":0,"3292881":0,"33":0,"331":0,"332":0,"333":0,"334":0,"335":0,"34":0,"340":0,"35":0,"36":0,"37":0,"38":0,"39":0,"4":0,"40":0,"41":0,"411":0,"412":0,"41639287":0,"42":0,"421":0,"422":0,"423":0,"42694882":0,"429":0,"4294967295":0,"43":[1,7],"44":0,"45393088":0,"45589904":0,"46036911":0,"46290469":0,"46795189":0,"5":0,"51":0,"511":0,"512":0,"519284":0,"52":0,"521":0,"522":0,"523":0,"554":0,"57":0,"572":0,"582":0,"590":0,"590326":0,"6":0,"614":0,"61707":0,"65535":0,"675":0,"68368468":0,"7":0,"729":0,"76769064":0,"8":0,"81258967":0,"818":0,"86747235":0,"87945694":0,"88746967":0,"89827633":0,"9":0,"9280":0,"9430203":0,"94553375":0,"950":0,"9a":0,"case":[4,6],"class":[4,5,7],"default":[1,6,7],"float":[4,7],"function":[4,5,7],"import":[0,4],"new":[1,2,4,7],"return":[4,5,6],"true":[4,6],"try":4,A:[1,4,5,7],AT:0,BE:0,Be:4,By:[6,7],For:4,If:[0,1,4,5,6],It:4,One:1,Or:1,The:[0,1,2,4,6,7],To:[1,2,4,5,7],Will:4,_:0,__main__:5,_names_:5,_no_:4,_not_:4,ab:0,access:[0,1],accident:[1,4],acquisit:4,acquisition_d:0,acquisition_tim:0,actual:4,agricultur:0,agro:[0,4],airport:0,all:[1,2,4,5,6,7],allow:1,alreadi:4,also:[1,2,4],although:1,alwai:7,an:4,ani:[1,4],annual:0,api:2,appli:4,applic:[0,2,5],approach:4,ar:[0,1,2,4,5],arabl:0,archiv:[1,4],area:[0,4],arg:4,artifici:0,associ:0,assum:4,austria:[0,5,6],avail:[6,7],avoid:4,awar:4,axi:4,b01:0,b02:0,b03:0,b04:0,b05:0,b06:0,b07:0,b08:0,b09:0,b11:0,b12:0,b8a:0,b:0,band:[0,7],band_stat:0,band_stats_float32:0,bare:0,base:5,basic:5,beach:0,belgium:[0,5,6],belong:6,ben:4,ben_19_labels_to_multi_hot:[1,4],ben_43_labels_to_multi_hot:[1,4],ben_build_csv_set:[2,7],ben_channel:0,ben_cloudy_or_shadowy_patches_count:0,ben_complete_s:0,ben_constant_prompt:[0,5],ben_constants_prompt:7,ben_no_19_class_target_count:0,ben_patch_size_m:0,ben_recommended_s:0,ben_rgb_channel:0,ben_s1_band_r:0,ben_s1_r:0,ben_s1_v1_0_json_kei:0,ben_s2_band_r:0,ben_s2_r:0,ben_s2_v1_0_json_kei:0,ben_snowy_patches_count:0,ben_validate_s1_root_dir:1,ben_validate_s2_root_dir:1,berri:0,best:4,better:7,bigearth:0,bigearthnet:[4,5,6],bigearthnet_common:[0,4,5,6,7],bigearthnet_gdf_build:[1,4],binari:7,bodi:0,bool:[4,6],broad:0,build:[2,4,6],build_csv_set:6,build_set:6,burnt:0,bz2:4,cach:4,call:[2,5,7],can:[0,1,2,4,7],caus:7,ch:0,channel:7,check:[0,1,4],clc_code_to_clc_lv1:0,clc_code_to_clc_lv2:0,clc_code_to_clc_lv3:0,clc_lv1_count:0,clc_lv1_label:0,clc_lv1_to_clc_cod:0,clc_lv2_count:0,clc_lv2_label:0,clc_lv2_to_clc_cod:0,clc_lv2_to_lv1:0,clc_lv3_count:0,clc_lv3_label:0,clc_lv3_to_clc_cod:0,clc_lv3_to_lv1:0,clc_lv3_to_lv2:0,cli:[1,5],click:5,cloud:[4,7],cloudi:7,coastal:0,coher:4,collect:[4,7],column:[4,5],comerci:0,command:[2,7],commerci:0,common:[1,4],compact:4,compil:0,complet:4,complex:[0,7],compress:4,conda:7,conifer:0,consist:5,constant:6,constraint:7,construct:0,contain:[2,4,6,7],content:1,continu:0,control:2,conveni:4,convent:4,convert:[1,4,7],coordin:[0,4],correct:4,correspond:[1,4],corresponding_s2_patch:[0,4],could:4,countri:[0,1,2,4,5,6,7],countries_iso_a2:0,coupl:1,cours:0,creat:[6,7],crop:0,csv:[2,4,6,7],cultiv:0,d:0,dai:0,data:[0,1,4,7],dataset:[4,7],date:4,datetim:4,defin:[0,4,5],delet:[1,4],depend:7,detect:0,determinist:[1,6],dict:4,dictionari:[4,5],differ:0,dir_path:4,directli:[0,1,2,5],directori:4,directorypath:4,discontinu:0,dl:[2,7],doe:6,download:0,drive:1,due:1,dump:0,dune:0,dure:[2,7],e:7,each:[1,4],easili:7,effici:1,either:4,empti:[1,2,4],encod:[1,4,7],ensur:[2,4,6],entir:4,entri:4,enumer:4,environ:7,error:4,especi:1,estuari:0,etc:7,exampl:[4,5],exist:[1,4],expect:4,extended_ben_s1_gdf:4,extended_gdf:4,extract:[0,1],fabric:0,facil:0,fail:1,fall:[5,6],fals:[4,6],fast:4,fi:0,field:0,file:[1,2,4,6,7],file_path:[2,6,7],filepath:4,filter:7,filter_patches_by_countri:[2,6],filter_patches_by_season:[2,6],filter_patches_by_split:[2,6],find:[1,4],finland:[0,5,6],first:1,fix:4,flat:0,flexibl:1,float32:0,float64:0,follow:[0,1],forest:0,forestri:[0,4],format:4,found:5,frequent:[1,4],from:[0,2,4,5,7],fruit:0,funtion:4,gener:[2,6],geopanda:4,get:[1,7],get_all_s1_patch:6,get_all_s2_patch:6,get_complete_s1_to_s2_patch_name_map:4,get_complete_s2_to_s1_patch_name_map:4,get_original_split_from_patch_nam:[1,4],get_patches_to_country_map:[1,4],get_patches_to_season_map:[1,4],get_s1_patch_directori:4,get_s1_patches_from_original_test_split:4,get_s1_patches_from_original_train_split:4,get_s1_patches_from_original_validation_split:4,get_s1_patches_with_cloud_and_shadow:4,get_s1_patches_with_no_19_class_target:4,get_s1_patches_with_seasonal_snow:4,get_s2_patch_directori:4,get_s2_patches_from_original_test_split:4,get_s2_patches_from_original_train_split:4,get_s2_patches_from_original_validation_split:4,get_s2_patches_with_cloud_and_shadow:4,get_s2_patches_with_no_19_class_target:4,get_s2_patches_with_seasonal_snow:4,get_s2patches_with_no_19_class_target:4,give:0,given:[1,4,5,6],glacier:0,good:[5,6],grassland:0,grdh:0,green:0,ground:0,group:6,grove:0,gt:0,guarante:1,guess:5,gz:0,ha:7,happen:4,hard:1,have:[4,7],header:[4,6],heathland:0,help:[0,1,2,4,7],helper:4,herbac:0,heterogen:0,high:[0,7],higher:1,highli:4,hood:5,hot:[1,4,7],http:0,hv:0,i:7,ideal:6,ie:0,ignor:4,illeg:4,implement:1,includ:4,incomplet:1,index:4,industri:0,infer:4,inland:0,inp:4,input:[1,4],integ:7,integr:1,interact:7,interest:7,interferometr:0,intermedi:4,intertid:0,ireland:[0,5,6],irrig:0,is_cloudy_shadowy_patch:[1,4],is_snowy_patch:[1,4],isna:4,issu:[1,4,7],iter:4,its:4,iw:0,json:[1,4,7],json_fp:4,keep:5,kei:4,keyerror:4,kosovo:[0,5,6],label:[0,4,7],lagoon:0,land:0,leav:0,leisur:0,let:7,level:[0,1,7],librari:[1,5,7],like:7,line:7,list:[1,4,5,6,7],lithuania:[0,5,6],littl:0,lly:4,load:4,look:[0,5,7],lot:4,lry:4,lt:0,lu:0,luxembourg:[0,5,6],m:7,mani:1,map:[1,4],marin:0,marsh:0,match:5,max_values_by_dtype_str:0,mean:[0,7],metadata:7,mine:0,miner:0,mix:0,modifi:4,month:[0,2,7],moor:0,more:[2,7],most:[0,5,7],msil2a:0,multi:[1,4,7],n:0,name:[4,5,6,7],natur:[0,4,6],necessari:4,necessarili:4,net:0,network:0,new_label:[0,4],new_labels_to_idx:0,nice:0,no_19_label_target:4,nomenclatur:[1,4,7],non:0,none:[0,4],nope:3,note:4,object:4,obstruct:4,occupi:0,ocean:0,offici:5,old2new_label:[1,4],old2new_labels_dict:0,old:[1,4,7],old_label:[0,4],old_labels_to_idx:0,oliv:0,one:1,onli:[1,2,4,6,7],open:0,option:4,order:4,origin:[4,7],orign:6,other:[4,6],otherwis:4,output:[0,4,6],p:0,packag:[1,7],parquet:4,pars:4,parse_datetim:4,parser:7,partial:4,pastur:0,patch:[2,4,6,7],patch_from_russia:0,patch_in_terrotorial_wat:0,patch_nam:4,patches_with_no_19_class_target:4,path:[4,6],pathlib:[4,6],pattern:0,peatbog:0,perform:4,perman:0,perpetu:0,person:7,pip:7,place:7,plantat:0,point:6,port:0,portug:[0,4,5,6],pre:5,present:4,princip:0,print:[0,5],print_all_const:[0,5],process:0,produc:6,product:0,programmat:2,project:0,properti:1,provid:[1,4,7],pt:0,publicli:6,pydant:4,pypi:7,python:[2,7],queri:1,quick:0,quickli:[0,1,2,4,5,7],rail:0,rais:4,rang:0,raw_ben_s2_gdf:4,raw_gdf:4,re:[0,4],read:[1,4],read_parquet:4,read_s1_json:[1,4],read_s2_json:[1,4],recommend:1,reduc:7,refer:[1,4],refin:2,regener:4,relat:7,relev:[1,7],remov:[2,7],remove_unrecommended_dl_patch:6,renam:4,represent:5,requir:4,resolut:0,resourc:4,restrict:6,result:[4,6],retriev:[1,4],rice:0,rich:5,road:0,rock:0,row:6,rs:0,s1:[0,1,4,5,6,7],s1_name:4,s1_patch_nam:4,s1_to_s2_patch_nam:[1,4],s1_v1:4,s2:[0,1,2,4,5,6,7],s2_name:4,s2_patch_nam:4,s2_to_s1_patch_nam:[1,4],s2b_msil2a_20170814t100029_33_77:0,s2b_msil2a_20180221t093029_65_1:0,safe:[1,4,7],salin:0,salt:0,sand:0,scene_sourc:0,sclerophyl:0,sea:0,search:7,season:[1,2,4,5,6,7],see:0,seminatur:0,sentinel:[0,2,4,5,6,7],sentinel_miss:0,sentinel_sourc:6,sentinelsourc:[5,6],sequenc:6,serbia:[0,2,5,6,7],server:1,set:4,shadow:[4,7],should:[1,4,5,7],show:5,shrub:0,signific:0,silent:[1,4],simpl:[4,5],simpli:[0,5],simultan:1,singl:[5,7],site:0,size:1,slow:1,small:5,smart_pprint:5,snow:[0,4,7],snowi:7,sort:6,sourc:5,space:0,spars:0,specif:5,spent:7,split:[2,4,5,6,7],sport:0,spring:[2,5,6,7],start:6,statist:7,std:0,step:1,still:4,store:7,str:[4,6],strictli:4,string:[4,7],style:[4,6],subset:[2,4,6,7],summer:[2,5,6,7],surfac:0,swath:0,switzerland:[0,5,6],t:0,tabl:[0,5],tar:0,target:4,termin:0,test:[4,5,6],thei:[1,4],them:7,thi:[4,6,7],those:[4,6],tile_sourc:0,time:7,to_csv:4,to_iso_a2:5,tool:[1,2,7],train:[4,5,6],transit:0,transport:0,tree:0,tri:[5,7],two:5,type:[4,5],typo:4,uint16:0,uint32:0,uint8:0,uncommon:1,under:5,union:4,unit:0,unknown:4,unrecommend:[2,7],up:5,urban:0,url:[0,7],us:[1,2,4,5,6,7],use_s2_patch_nam:4,user:[4,7],userwarn:4,usual:1,util:2,v1:0,v:0,valid:[4,5,6],validate_ben_s1_root_directori:4,validate_ben_s2_root_directori:4,valu:[0,4,5],variabl:[0,5],varianc:7,variou:7,vector:4,veget:0,verbos:0,verifi:4,version:4,via:7,view:7,vineyard:0,visual:0,wa:6,wai:[0,1],want:1,warn:4,water:0,were:4,wetland:0,when:[1,4],where:4,wherea:5,whether:4,which:4,wide:0,winter:[2,5,6,7],woodland:0,work:[1,4,7],wors:1,wrapper:[1,5],write_separate_split:6,xk:0,year:[0,5],you:[0,1,2,4],your:2},titles:["BigEarthNet Constants","BigEarthNet Base Functions","BigEarthNet Set Builder Functions","API","Base","Constants","Sets","BigEarthNet Common"],titleterms:{"function":[1,2],api:3,base:[1,4],bigearthnet:[0,1,2,7],builder:2,common:7,constant:[0,5,7],gener:7,instal:7,label:1,metadata:1,name:1,pars:1,patch:1,review:7,set:[2,6,7],util:1,valid:1}})