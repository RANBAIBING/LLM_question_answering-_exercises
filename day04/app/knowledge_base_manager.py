import os

from .models import KnowledgeBaseModel, FileModel, FileChunkModel


# 新建知识库
def new_add_knowledge(knowledge_name, chunk_size, chunk_overlap):
    try:
        KnowledgeBaseModel.objects.create(knowledge_base_name=knowledge_name, maximum_block_length=chunk_size,
                                          repeated_character_length=chunk_overlap)
    except Exception as e:
        print(e)
        return "该知识库已存在"
    return "新知识库创建成功"


# 添加文件、文件分块、向量化、创建向量化知识库或存入向量化知识库
def receive_front_end_file(file, knowledge_id):
    # 获取该知识库信息，即相关参数
    try:
        knowledge_base = KnowledgeBaseModel.objects.get(id=knowledge_id)
    except Exception as e:
        print(e)
        return "该知识库不存在"

    # 将前端传来的二进制文件存入django中
    print(file.name)
    with open(file.name, "wb") as f:
        f.write(file.read())

    # 在分割前先判断文件类型，根据对应类型进行切割，支持txt、pdf、docx格式
    file_type = file.name.split(".")[-1]
    print(file_type)
    if file_type == "txt":
        from langchain_community.document_loaders import TextLoader
        # 实例化TextLoader对象
        loader = TextLoader(file.name, encoding="utf-8")
        # 加载文档
        docs = loader.load()
        print(docs)

    elif file_type == "pdf":
        from langchain_community.document_loaders import PyPDFium2Loader

        # 加载PDF文件
        loader = PyPDFium2Loader(file.name)
        docs = loader.load()
        print(docs)
    elif file_type == "docx":
        from langchain_community.document_loaders import Docx2txtLoader

        # 加载docx
        loader = Docx2txtLoader(file.name)
        docs = loader.load()
        print(docs)
    else:
        return "文件类型错误"

    # 导入分割类
    from langchain.text_splitter import CharacterTextSplitter

    # 实例化
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=knowledge_base.maximum_block_length,
                                          chunk_overlap=knowledge_base.repeated_character_length)
    # 对文件内容进行分割
    docs_splitter = text_splitter.split_documents(docs)
    print(docs_splitter)

    # 引入向量化的类
    from langchain_community.vectorstores import Chroma
    from langchain.embeddings.dashscope import DashScopeEmbeddings

    # 实例化
    embeddings = DashScopeEmbeddings()

    # 获取该知识库中是否有数据
    knowledge_base_file_list = knowledge_base.file_knowledge_base.all()
    if not knowledge_base_file_list:
        # 创建向量数据库,向量化文档
        db = Chroma.from_documents(docs_splitter, embeddings, persist_directory="./chroma/"+knowledge_base.knowledge_base_name)
        db.persist()

    else:
        # 对数据进行加载
        db = Chroma(persist_directory="./chroma/"+knowledge_base.knowledge_base_name, embedding_function=embeddings)
        print(db.__len__())

        # 添加文档
        # 添加文档的方法
        db.add_documents(docs_splitter)
        print(db.__len__())

    # 将文件内容信息存入mysql数据库
    knowledge_base_file = FileModel.objects.create(file_name=file.name,
                                                   file_type=file_type,
                                                   file_content=docs[0].page_content,
                                                   knowledge_base=knowledge_base)

    # 将分割后的文件内容存入分割表中
    for item in docs_splitter:
        FileChunkModel.objects.create(file=knowledge_base_file,
                                      file_chunk_content=item.page_content,
                                      knowledge_base=knowledge_base,)

    # 删除前端存入django的文件
    os.remove(file.name)

    return "文件添加到各库成功"


# 获取用于展示的所有知识库
def get_all_knowledge_base():
    knowledge_base_list = KnowledgeBaseModel.objects.all()
    return knowledge_base_list


# 获取用于展示的该知识库内的所有文件
def get_all_knowledge_base_file(knowledge_base_id):
    try:
        knowledge_base = KnowledgeBaseModel.objects.get(id=knowledge_base_id)
    except Exception as e:
        print(e)
        return "该知识库不存在"
    knowledge_base_file_list = knowledge_base.file_knowledge_base.all()
    knowledge_base_name = knowledge_base.knowledge_base_name
    return knowledge_base_file_list, knowledge_base_name


# 获取用于展示的该文件的所有分块表
def get_all_knowledge_base_file_chunk(knowledge_base_file_id):
    try:
        knowledge_base_file = FileModel.objects.get(id=knowledge_base_file_id)
    except Exception as e:
        print(e)
        return "该文件不存在"
    knowledge_base_file_chunk_list = knowledge_base_file.file_chunk.all()
    file_name = knowledge_base_file.file_name
    return knowledge_base_file_chunk_list, file_name


# 删除知识库
def delete_knowledge_base(knowledge_base_id):
    # 输出mysql中的知识库
    try:
        knowledge_base = KnowledgeBaseModel.objects.get(id=knowledge_base_id)
    except Exception as e:
        print(e)
        return "该知识库不存在"

    """
    # 删除对应向量数据库
    # 删库前刷新一下当前正在使用的库
    # 引入向量化的类
    from langchain_community.vectorstores import Chroma
    from langchain.embeddings.dashscope import DashScopeEmbeddings
    # 实例化
    embeddings = DashScopeEmbeddings()
    # 对数据进行加载
    db = Chroma(persist_directory="./chroma/" + "用于删库前刷新", embedding_function=embeddings)
    print(db.__len__())
    """

    if knowledge_base.file_knowledge_base.all():
        # 递归删除文件夹内所有内容
        for root, dirs, files in os.walk("./chroma/"+knowledge_base.knowledge_base_name, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))

        # 删除现在空的文件夹
        os.rmdir("./chroma/"+knowledge_base.knowledge_base_name)

    knowledge_base.delete()

    return "该知识库删除成功"


