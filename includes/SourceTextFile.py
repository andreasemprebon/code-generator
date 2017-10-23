from includes.Include import Include
from comments.Comment import Comment
from libraries.Library import Library, ROSBase_TF_Interface


class SourceTextFile(Include):
    def __init__(self, _associated_class, file_name, function_name):
        super().__init__(_associated_class, file_name)

        self.function_name = function_name
        self.function_type = None
        self.function_parameters = []

    def setFunctionType(self, function_type):
        self.function_type = function_type

        if self.function_type.namespace != None:
            lib = Library()
            lib.setPath("{}/{}.h".format(self.function_type.namespace, self.function_type.type_name))
            self.addLibrary(lib)

    def addFunctionParameter(self, param):
        self.function_parameters.append(param)

        if param.type.namespace != None:
            lib = Library()
            lib.setPath("{}/{}.h".format(param.type.namespace, param.type.type_name))
            self.addLibrary(lib)

    def isEqualTo(self, another_object):

        if self.file_name != another_object.file_name:
            return False

        if self.function_name != another_object.function_name:
            return False

        if not self.function_type.isEqualTo( another_object.function_type ):
            return False

        return True

    def generateInlineCode(self):
        code = ""

        code += "{}(".format(self.function_name)

        if self.associated_class.node_configuration != None:
            if self.associated_class.node_configuration.has_variables:
                code += " is.vars(),"

            if self.associated_class.node_configuration.has_parameters:
                code += " is.params(),"

            for p in self.function_parameters:
                code += " {},".format(p.name)

            if self.uses_tf:
                code += " tf,"

            # Rimuovo l'ultima virgola
            code = code[:-1]

        code += ")"

        return code

    def generateCode(self):
        # Subito prima di generare il codice devo aggiungere la libreria con la node configuration
        # se serve ed è usata
        if self.associated_class.node_configuration != None:
            lib = Library()
            lib.setPath( self.associated_class.node_configuration.getSourceLibraryPath() )
            self.addLibrary( lib )

        if self.uses_tf:
            self.addLibrary( ROSBase_TF_Interface() )

        code = ""

        for l in self.libraries:
            code += l.generateCode()

        code += "{} {}(".format( self.function_type.generateCode(), self.function_name )

        if self.associated_class.node_configuration != None:

            if self.associated_class.node_configuration.has_variables:
                code += " Variables_ptr v,"

            if self.associated_class.node_configuration.has_parameters:
                code += " Parameters_ptr p,"

            for p in self.function_parameters:
                code += " {},".format(p.generateCode())

            if self.uses_tf:
                code += " ros_base::TransformationFrames * tf,"

            # Rimuovo l'ultima virgola
            code = code[:-1]

        code += ") {\n"

        # Commento per dire dove inserire il codice
        code += "\n"
        c = Comment()
        c.setComment("Insert here your custom code")
        code += "".join(["\t{}\n".format(c_lin) for c_lin in c.generateCode().split("\n")])

        code += "}\n"

        return code