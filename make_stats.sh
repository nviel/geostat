#!/bin/bash
# -----------------------------------------------------------------------------
# TODO: o passer le chemin des données en parametre ou faire un fichier de conf.
#       o simplifier la configuration des cartes (il y a trop de fichiers)
#       o générer les stats, cartes et rapport dans l'arborescence définitive
#       o générer les cartes manquantes (PARCELLAIRE, CARTES, TOUTES)
#       o générer les DOM
# -----------------------------------------------------------------------------

#gesion des parametres
if [[ $# -eq 0 ]]
then
  jour=`date -d yesterday +%y%m%d`
elif [[ $# -eq 1 ]]
then
  jour=$1
else
  echo "usage: make_stats.sh [date] (date format: AAMMDD)"
  exit 1
fi


# Initialisation
SCRIPTPATH="${0%/*}"
testlog_root="$SCRIPTPATH/test/log_access_localtest"
work_root="/media/local_data/geostats" #FIXME: depend de la machine!
liste_machines="wpgppe40s wpgppe41s wpgppe42s wpgppe43s wpgppe44s wpgppe45s wpgppe46s wpgppe47s"
#liste_machines="wpgppe40s"


if [ ! -d $work_root ]
then
  echo "J'ai pas trouve l'espace de travail $work_root"
  exit 1
fi
log_root="$work_root/log"

# recuperation des logs par machine et generation des stats par machine
for machine in $liste_machines 
do
  mkdir -p $log_root/$jour/$machine
  cd $log_root/$jour/$machine
  log_file="access.$jour.$machine"
  if [ $jour = 'TEST' ]
  then
    cp $testlog_root/$machine/access.log ./$log_file
  else
    copy_log $machine $jour
    gunzip "$log_file.gz"
  fi
  sort_log.py $log_file 
  rm $log_file

  for f in bad_request.txt bad_signature_2D.txt bad_signature_3D.txt bad_signature_m.txt echec.txt
  do 
    cat $f >> ../$f
    rm $f
  done
  # FIXME: il faudrait faire des rapports fusionner plutot que de les conserver par machine.
  mv report.txt ../$machine.report.txt
done

#echo "fin du traitement des log. En attente d'un go pour la suite"
#read toto

# fusion des rapports de 403
cd $log_root/$jour
report_list=`find . -name forbiddenReport.txt`
report_fusion.py ./forbiddenReport.txt $report_list

#echo "fin de la fusion des rapport 403. En attente d'un go pour la suite"
#read toto

rm $report_list 

# fusion des stats par machine en stats du jour
cd $log_root/$jour
stats_list=`find ./wpgppe* -not -name '*.txt' | cut -b 13- | sort | uniq`  
mkdir ALL
for stat in $stats_list
do
  fusion_list=`find . -name $stat`
  stats_fusion.py ./ALL/$stat $fusion_list
done

# suppression des stats par machine.
rm -fr $liste_machines

# generation des cartes
#FIXME: Revoir la facon de generer les images. Faire un fichier de conf par images est trop lourd.
#  
echo "build_map.py $SCRIPTPATH/ressources/cartes/FXX_ORTHOIMAGERY.ORTHOPHOTOS_8-15.map"    
build_map.py $SCRIPTPATH/ressources/cartes/FXX_ORTHOIMAGERY.ORTHOPHOTOS_8-15.map
# build_map.py $SCRIPTPATH/ressources/cartes/FXX_ORTHOIMAGERY.ORTHOPHOTOS_10.map
# build_map.py $SCRIPTPATH/ressources/cartes/FXX_ORTHOIMAGERY.ORTHOPHOTOS_11.map
# build_map.py $SCRIPTPATH/ressources/cartes/FXX_ORTHOIMAGERY.ORTHOPHOTOS_12.map
# build_map.py $SCRIPTPATH/ressources/cartes/FXX_ORTHOIMAGERY.ORTHOPHOTOS_13.map
# build_map.py $SCRIPTPATH/ressources/cartes/FXX_ORTHOIMAGERY.ORTHOPHOTOS_14.map
# build_map.py $SCRIPTPATH/ressources/cartes/FXX_ORTHOIMAGERY.ORTHOPHOTOS_15.map
# build_map.py $SCRIPTPATH/ressources/cartes/FXX_ORTHOIMAGERY.ORTHOPHOTOS_16.map
# build_map.py $SCRIPTPATH/ressources/cartes/FXX_ORTHOIMAGERY.ORTHOPHOTOS_17.map
# build_map.py $SCRIPTPATH/ressources/cartes/FXX_ORTHOIMAGERY.ORTHOPHOTOS_18.map
# build_map.py $SCRIPTPATH/ressources/cartes/FXX_ORTHOIMAGERY.ORTHOPHOTOS_19.map

image_list=`ls *.png | sed "s/.png//"`
for image in $image_list
do
  mkdir -p $work_root/evol/$image
# mkdir -p $work_root/evol/$key/$terr/$layer/$level/
  ln -s $log_root/$jour/$image.png $work_root/evol/$image/$jour.png
# ln -s $log_root/$jour/$image.png $work_root/evol/$key/$terr/$layer/$level/$jour.png
done


# archivage des stats

# tri des fichiers pour ameliorer la compression.
# le gzip est beaucoup plus efficace quand on a trie les fichiers prealablement.
for stat in $stats_list
do
  sort ./ALL/$stat > ./ALL/${stat}.sorted
  rm ./ALL/$stat
  mv ./ALL/${stat}.sorted ./ALL/$stat
done
# compression
tar cvzf $jour.ALL.tgz ALL
rm -fr ALL

