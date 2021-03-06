from includes.SourceTextFile import SourceTextFile
from includes.SourceTextFunction import SourceTextFunction
import threads.AADLThreadFunctionsSupport as tfs
import re
from datatypes.Type import Void

# isMainThread()
# Funzione usata da AADLProcess, viene scritta qua per rendere uniforme il codice
def isMainThread(aadl_thread_type):
    main_thread = re.compile("main_loop([_a-zA-Z0-9:\.]*)\.impl", re.IGNORECASE)
    return (main_thread.match(aadl_thread_type) != None)

# In questa funzione è presente il nome del modulo e della classe che gestisce la creazione di quel
# particolare tipo di thread. Un caso di esempio è il seguente.
# Thread di tipo publisher.
# Il nome del modulo che lo gestisce è threads.Publisher
# Il nome della classe all'interno del modulo è Publisher
def getPythonClassFromAADLThreadType(aadl_thread_type):
    ###################
    ### MAIN THREAD ###
    ###################

    # Identifica il thread base da cui sono composti tutti gli elementi, questo thread è
    # passato al costruttore delle altre tipologie di thread in quanto contiene riferimenti
    # alle funzioni base come prepare, tearDown e errorHandling

    if isMainThread(aadl_thread_type):
        return "MainThread"

    #################
    ### PUBLISHER ###
    #################

    # Identifica i thread di tipo publisher
    publisher = re.compile("publisher([_a-zA-Z0-9:\.]*)\.impl", re.IGNORECASE)
    if publisher.match(aadl_thread_type) != None:
        return "Publisher"

    ##################
    ### SUBSCRIBER ###
    ##################

    # Identifica i thread di tipo subscriber
    subscriber = re.compile("callback([_a-zA-Z0-9:\.]*)\.impl", re.IGNORECASE)
    if subscriber.match(aadl_thread_type) != None:
        return "Subscriber"

    ############################
    ### SUBSCRIBER PUBLISHER ###
    ############################

    # Identifica i thread di tipo subscriber-publisher, thread che ripetono un
    # messaggio ricevuto in input su un topic su un topic di output dopo averlo
    # eventualmente manipolato
    subscriber = re.compile("call_pub([_a-zA-Z0-9:\.]*)\.impl", re.IGNORECASE)
    if subscriber.match(aadl_thread_type) != None:
        return "SubscriberPublisher"

    ######################
    ### SERVICE CLIENT ###
    ######################

    # Identifica i thread di tipo service client
    #service_client = re.compile("client([_a-zA-Z0-9:\.]*)\.impl", re.IGNORECASE)
    #if service_client.match(aadl_thread_type) != None:
    #    return "ServiceClient"

    ######################
    ### SERVICE SERVER ###
    ######################

    # Identifica i thread di tipo service server
    service_server = re.compile("service_provider([_a-zA-Z0-9:\.]*)\.impl", re.IGNORECASE)
    if service_server.match(aadl_thread_type) != None:
        return "ServiceServer"

    #############
    ### TIMER ###
    #############

    # Identifica i thread di tipo publisher
    publisher = re.compile("timer([_a-zA-Z0-9:\.]*)\.impl", re.IGNORECASE)
    if publisher.match(aadl_thread_type) != None:
        return "Timer"

    return None


# Classe da cui ereditano tutti i thread
class AADLThread():
    def __init__(self, _system_root, _process, _thread, _associated_class):
        # AADLProcess a cui un AADLThread fa riferimento
        self.associated_class = _associated_class

        # Processo e thread relativi
        self.system_root    = _system_root
        self.process        = _process
        self.thread         = _thread

        # Tipo thread
        self.type       = tfs.getType(self.thread)

        # Nome del thread
        self.name       = tfs.getName( self.thread )

        # TF
        self.thread_uses_tf = False

    def createSourceTextFileFromSourceText(self, source_text, source_name, function_type = Void()):
        if source_text == None or source_name == None:
            return None

        source_text_file = self.associated_class.getSourceFile( source_text )

        if source_text_file == None:
            source_text_file = SourceTextFile(self.associated_class, source_text)
            self.associated_class.addSourceFile(source_text_file)

        # Se ho già la funzione presente nel file, non la devo ri-creare
        if source_text_file.hasFunctionFromName( source_name ):
            source_text_function = source_text_file.getFunctionFromName( source_name )
        else:
            source_text_function = SourceTextFunction(self.associated_class, source_text_file, source_name)
            source_text_function.setFunctionType( function_type )

            source_text_file.addFunction( source_text_function )

        return source_text_function

    def setUsesTransformationFrame(self):

        # Controllo che il system in cui è incluso il process che include il thread abbia
        # un subcomponent di tipo tf
        if not tfs.hasTransformationFrameEnabledInSystem(self.system_root):
            self.associated_class.setUsesTransformationFrame(False)
            return False

        # Controllo che ho una connessione che parte dal mio thread ed esce verso il
        # process di tipo transformation frame
        tf_source_port_name = "tf"
        tf_connection_port_info = tfs.getConnectionPortInfoBySource(self.process, self.type, tf_source_port_name)

        # Il thread NON usa sicuramente i transformation frame
        if tf_connection_port_info == None:
            self.associated_class.setUsesTransformationFrame(False)
            return False

        (parent_name, parent_port) = tfs.getDestFromPortInfo(tf_connection_port_info)

        if not tfs.isConnectedToSystemTransformationFrame(self.system_root, parent_name, parent_port):
            self.associated_class.setUsesTransformationFrame(False)
            return False

        self.associated_class.setUsesTransformationFrame(True)
        return True

    # getDefaultTopicName
    # A partire dal thread attuale, cerca il nome di default del topic associato alla connessione
    # Ha bisogno del nome della porta specificato per quel particolare thread (è un nome statico
    # deciso a priori). I parametri input, output definiscono se la porta da cercare è una porta
    # di input (nel caso di un Subscriber), oppure di output (nel caso di un Publisher)
    def getDefaultTopicName(self, thread_port_name, input=False, output=False):
        if not input and not output:
            return (False, "No direction specified")

        thread_name = tfs.getName(self.thread)

        # Ottengo tutte le connesioni di un processo che mappano la porta specificata in process_port_name
        # del thread associato a questo processo con una porta qualunque del thread.
        connections = tfs.getAllConnectionsPerPort(self.process, thread_name, thread_port_name,
                                                    input=input,
                                                    output=output)

        names = []

        # Per ognuna delle connesioni trovate sopra bisogna cercare la porta verso cui (o da cui) è presente
        # la connessione e poi cercare la proprietà del topic name su di essa
        for c in connections:

            process_port_name = None
            # Ottengo il nome della porta
            if input:
                port_info = tfs.getPortInfoByDestPortInfo(c, thread_name, thread_port_name)
                (process_name, process_port_name) = tfs.getSourceFromPortInfo(port_info)
            elif output:
                port_info = tfs.getPortInfoBySourcePortInfo(c, thread_name, thread_port_name)
                (process_name, process_port_name) = tfs.getDestFromPortInfo(port_info)

            # La porta è una feature, quindi si usa getFeatureByName
            process_port = tfs.getFeatureByName(self.process, process_port_name)

            (topic_namespace, topic_name) = tfs.getDefaultTopicName(process_port)

            if topic_namespace == None or topic_name == None:
                return (False, "Unable to get topic name")

            names.append(topic_name)

        names = list(set(names)) # Rimuovo i duplicati

        if len(names) < 1:
            return (False, "No topic name defined")

        if len(names) > 1:
            return (False, "Multiple topic names defined")

        self.topic = names[0]

        return (True, "")

    def populateData(self):
        raise NotImplementedError("populateData deve essere implementata da ogni subclass di Thread")