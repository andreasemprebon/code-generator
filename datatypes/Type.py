from CObject import CObject

# Import per classi già definite
import libraries.Library as lib

class Type(CObject):
    def __init__(self, _associated_class = None, _namespace = None, _type_name = None ):
        super().__init__( _associated_class )
        self.isConst    = False
        self.namespace  = _namespace
        self.type_name  = _type_name
        self.library    = None
        self.afterTypeName = ""

    def setAfterTypeName(self, _text):
        self.afterTypeName = _text

    def setConst(self, _const = True):
        self.isConst = _const

    def setNamespace(self, _namespace):
        self.namespace = _namespace

    def setTypeName(self, _type_name):
        self.type_name = _type_name

    def setLibrary(self, _library):
        self.library = _library
        self.associated_class.addLibrary( _library )

    def removeLibrary(self):
        self.associated_class.removeLibrary( self.library )
        self.library = None

    def shouldImportLibrary(self):
        return (self.library != None)

    def isEqualTo(self, another_type):
        if self.isConst != another_type.isConst:
            return False

        if self.namespace != another_type.namespace:
            return False

        if self.type_name != another_type.type_name:
            return False

        if self.library != None:
            if not self.library.isEqualTo(another_type.library):
                return False
        else:
            if another_type.library != None:
                return False

        if self.afterTypeName != another_type.afterTypeName:
            return False

        return True

    def generateCodeForMessageAndService(self):
        if self.namespace == None:
            return self.type_name
        else:
            return "{}/{}".format(self.namespace, self.type_name)

    def generateCode(self):
        const_str = ""
        if self.isConst:
            const_str = "const "

        if ( self.namespace == None ):
            return "{}{}{}".format(const_str, self.type_name, self.afterTypeName)
        else:
            return "{}{}::{}{}".format(const_str, self.namespace, self.type_name, self.afterTypeName)

class Object(Type):
    def __init__(self, _associated_class, name):
        super().__init__( _associated_class )
        self.setTypeName( name )

class Nothing(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setTypeName( "" )

class Void(Type):
    def __init__(self, _associated_class = None):
        super().__init__( _associated_class )
        self.setTypeName( "void" )

class Int(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setTypeName( "int" )

class Int64(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setTypeName( "int64" )

class Bool(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setTypeName( "bool" )

class Double(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setTypeName( "double" )

class Float64(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setTypeName( "float64" )

class String(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setNamespace( "std" )
        self.setTypeName( "string" )

class StdMsgsString(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setNamespace( "std_msgs" )
        self.setTypeName( "String" )

class MsgSrv_String(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setTypeName( "string" )

class Char(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setTypeName( "char" )

class PointerToCharPointer(Type): #char **
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setTypeName( "char**" )

class ROS_Time(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setNamespace("ros")
        self.setTypeName( "Time" )

class MsgSrv_Time(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setTypeName( "time" )

class ROS_TimerEvent(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setConst(_const = True)
        self.setNamespace("ros")
        self.setTypeName( "TimerEvent&" )

class ROS_Timer(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setNamespace("ros")
        self.setTypeName( "Timer" )

class ROS_Publisher(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setNamespace("ros")
        self.setTypeName( "Publisher" )

class ROS_Subscriber(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setNamespace("ros")
        self.setTypeName( "Subscriber" )

class ROS_ServiceClient(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setNamespace("ros")
        self.setTypeName( "ServiceClient" )

class ROS_ServiceServer(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setNamespace("ros")
        self.setTypeName( "ServiceServer" )

class ROS_ServiceServer_Request(Type):
    def __init__(self, _associated_class, namespace):
        super().__init__( _associated_class )
        self.setNamespace(namespace)
        self.setTypeName( "Request" )

class ROS_ServiceServer_Response(Type):
    def __init__(self, _associated_class, namespace):
        super().__init__( _associated_class )
        self.setNamespace(namespace)
        self.setTypeName( "Response" )

class ROSBase_TransformationFrames(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setNamespace("ros_base")
        self.setTypeName( "TransformationFrames" )

class ROSBase_PointerToTransformationFrames(Type):
    def __init__(self, _associated_class):
        super().__init__( _associated_class )
        self.setNamespace("ros_base")
        self.setTypeName( "TransformationFrames *" )