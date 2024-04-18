
# from operator import indexOf, truediv
import unreal, sys, time

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
progress_bar_percent = 0

# progressBarCount = 0

# meshBox = True
# matBox = True
# bpBox = True
# effectsBox = True
# audioBox = True
# foliageBox = True


# meshBox = False
# matBox = False
# bpBox = False
# effectsBox = False
# audioBox = False
foliageBox = False


meshBox = meshes
matBox = mats
bpBox = bps
effectsBox = fx
audioBox = audio
# foliageBox = foliage

def select_actors(actor_list):
    unreal.EditorLevelLibrary.set_selected_level_actors(actor_list)

def get_level_actors():
    # Get the list of all actors in the current level
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    # Create an empty list to store static mesh actors
    static_mesh_actors = []
    bp_actors = []
    effects_actors = []
    foliage_actors = []
    audio_actors = []
 
    # Loop through all actors in the level
    for actor in actors:
        if meshBox == True or matBox == True :
        # Check if the actor is a static mesh actor
            if isinstance(actor, unreal.StaticMeshActor):
                    # If it is, add it to the list
                    static_mesh_actors.append(actor)
        
        if bpBox == True:
            if isinstance(actor.get_class(), unreal.BlueprintGeneratedClass):
                bp_actors.append(actor) 
                # print("bp level actor: "+ actor.get_name())  

        if effectsBox == True:
            if isinstance(actor, unreal.NiagaraActor):
                effects_actors.append(actor)

        if foliageBox == True:
            if isinstance(actor, unreal.InstancedFoliageActor):
                foliage_actors.append(actor)
                # unreal.log(actor.get_full_name())

        if audioBox == True:
            if isinstance(actor, unreal.AmbientSound):
                audio_actors.append(actor)
                # unreal.log(actor.get_full_name())

  
 
    # Return nested array of actors
    all_actors = [static_mesh_actors, bp_actors, effects_actors, foliage_actors, audio_actors]
    # print("MESHES: " + str(all_actors[0]) + "\n\n\n\n BLUEPRINTS: " + str(all_actors[1]) + "\n\n\n\n EFFECTS: " + str(all_actors[2])+ "\n\n\n\n FOLIAGE: " + str(all_actors[3]))

    return all_actors

# get staticmesh from staticmeshactors
def get_actor_components():
    actors = get_level_actors() #all_actors = [static_mesh_actors, bp_actors, effects_actors, foliage_actors, audio_actors]
    # takes a list of static mesh actors and returns a list of the corresponding static meshes without duplicates in the list. Adds materials to the list of elements
    meshes = []
    blueprintAssets = []
    materials = []
    effects = actors[2]
    effects = []
    foliage = []
    audio = []

    #gets meshes and materials
    if meshBox == True or matBox == True :
       
        for actor in actors[0]:
            mesh_component = actor.static_mesh_component
            mesh = mesh_component.get_editor_property('StaticMesh')
            material = mesh_component.get_material(0)

            if mesh not in meshes: meshes.append(mesh)
            if material not in materials : materials.append(material)
   
   
    #gets meshes from blueprints
    if bpBox == True:
        for actor in actors[1]:
            blueprintAssets.append(actor)


    if effectsBox == True:
        for actor in actors[2]:
            component = actor.get_editor_property('NiagaraComponent')
            vfxAsset = component.get_asset()
            effects.append(vfxAsset)


    if foliageBox == True:
        for actor in actors[3]:
            
            foliage.append(actor)
            components = actor.get_all_child_actors(include_descendants=True)
            for component in components:
                print("component: ")
                print(component)

            for i in components:
                mesh = i.get_editor_property('StaticMesh')
                meshes.append(mesh)


    if audioBox == True:
        for actor in actors[4]:
            component = actor.audio_component
            myProperty = component.get_editor_property('Sound')
            audio.append(myProperty)
            print("property" + str(myProperty))

    myComponents = [meshes, blueprintAssets, materials, effects, foliage, audio]

    return myComponents
    
def get_all_assets_of_type():
    # Get all the assets in the project
    all_assets_of_type = []
    all_static_meshes = []
    all_bps = []
    all_materials = []
    all_effects = []
    all_foliage = []
    all_audio = []

    all_assets =  unreal.EditorAssetLibrary.list_assets("/Game/", True, False)

    #Add them if they are the correct types
    for item in all_assets:
        try:
            myItem = unreal.EditorAssetLibrary.load_asset(item)
        except:
            continue

        if meshBox == True and isinstance(myItem, unreal.StaticMesh):
            all_static_meshes.append(myItem)
        elif bpBox == True and isinstance(myItem, unreal.Blueprint ) and not isinstance(myItem, unreal.WidgetBlueprint) and not isinstance(myItem, unreal.EditorUtilityWidget):
            all_bps.append(myItem)
        elif matBox == True and isinstance(myItem, unreal.Material):
            all_materials.append(myItem)
        elif effectsBox == True and isinstance(myItem, unreal.NiagaraSystem):
            all_effects.append(myItem)
        elif foliageBox == True and isinstance(myItem, unreal.FoliageType):
            all_foliage.append(myItem)
        elif audioBox == True and isinstance(myItem, unreal.MetaSoundSource):
            all_audio.append(myItem)

    all_assets_of_type = [all_static_meshes, all_bps, all_materials, all_effects, all_foliage, all_audio]

    return all_assets_of_type


def delete_assets():
    # myComponents = [meshes, blueprintAssets, materials, effects, foliage, audio]
    # all_assets_of_type = [all_static_meshes, all_bps, all_materials, all_effects, all_foliage, all_audio]
    actorComponents = get_actor_components()
    allAssets = get_all_assets_of_type()
    progressBarSize = 0
    assets_to_delete =[]
    bps_to_delete =[]

    
    # handle bps
    if bpBox == True:
        myBpNames = []
        allBpNames = []
        for x in actorComponents[1]:
            myBpNames.append(x.get_class().get_name().replace("_C",""))
        for x in allAssets[1]:
            allBpNames.append(x.get_name())
        myBps = set(myBpNames) & set(allBpNames)

        for x in allAssets[1]:
            if x.get_name() not in myBps:
                bps_to_delete.append(x)

    index = 0
    count = 0
    progressCount = 0
    for i in allAssets:
        # skip over the blueprint list
        if count == 1:
            count +=1
            continue
        count2 = 0
        for j in i:
            progressCount +=1
            progressBarCount = progressCount/progressBarSize
            progress_bar_percent = progressBarCount

            # print(get_level_actors()[count][count2])

            if j not in actorComponents[count]:
                try:
                    assets_to_delete.append(j)

                except:
                    print("exception made at "+ str(j))
                    # print("_")
                    continue
                count2 +=1

                
                
        count +=1
    
    # ---- Delete assets called here ---- 
    
    if not assets_to_delete and not bps_to_delete:
        unreal.log(" -- No assets to delete -- ")

    if bpBox == True:
        print("Selected "+ str(len(assets_to_delete) + len(bps_to_delete)) + " assets: ")
        print("-------------------------------------")
        for i in bps_to_delete:
            unreal.log(i.get_name())

    else:
        print("Selected " + str(len(assets_to_delete)) + " assets: ")
        print("-------------------------------------")

    for i in assets_to_delete:
        unreal.log(i.get_name())

    



    

     
delete_assets()
