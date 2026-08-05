# PyTodo

A minimal terminal todo tool.

## Todo

包含数据类型

- id: int
- text: str
- start_time: datetime
- end_time: datetime
- priority: Priority

## 先构建思路

- 程序的名字该起个什么名字呢？
    PyTodo
- 需要哪些方法呢
    add   : append todo.
    delete: delete todo.
    list  : list all todo(sort).
    sort  : Choose a sorting method
    NONE  : if no args, enter tui model
    help  : show usage
- 不用文件来存储了，要用一个数据库
- 接收处理参数
