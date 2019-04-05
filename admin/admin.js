

let data_form = Vue.component("data_form", {
        name: "data_form",
        props: ["current_data", "stack", "dev"],
        delimiters: ["[[", "]]"],
        data: function () {
            return {
                tmp_value: this.current_data,
                single_line: true,
                expand: false,
                new_key_name: "",
                new_type: "Number"
            }
        },
        methods: {
            make_index_string: function(stack){
                let ret = "data";
                for(let k of stack){
                    ret += "[" + this.to_string(k)  + "]";
                }
                return ret;
            },
            get_data_type: function (_data) {
                if (_data === undefined) {
                    return "Undefined";
                }
                if (_data.type === undefined) {
                    if (_data instanceof Array) {
                        return "Array";
                    } else if (typeof _data == "string") {
                        return "String";
                    } else if (typeof _data == "number") {
                        return "Number";
                    } else {
                        return "Object";
                    }
                } else {
                    return _data.type;
                }
            },

            data_changed: function () {
                this.$emit("data_change", {stack: this.stack, value: this.get_data_type(this.current_data) === "Number"?this.tmp_value-0:this.tmp_value});
            },

            add_item_to_array: function (arr, item) {
                let ret = [];
                for (let i of arr) {
                    ret.push(i);
                }
                ret.push(item);
                return ret;
            },
            to_string: function (obj) {
                if (typeof obj == "string") {
                    return '"' + obj + "'";
                }
                return obj;
            },

            add_new : function () {
                alert(this.new_type);
                let app = this;
                if(this.get_data_type(this.current_data) === "Array"){
                    this.$emit("add_new_data", {src_type:"Array", key:this.new_key_name, item_type:this.new_type,stack:this.stack});
                }else if(this.get_data_type(this.current_data) === "Object"){
                    if(this.new_key_name.length === 0){
                        layui.use("layer", function () {
                            let layer = layui.layer;
                            layer.msg("请先输入属性名称！", {icon: 2});
                        })
                    } else if(this.current_data[this.new_key_name] !== undefined) {
                        layui.use("layer", function () {
                            let layer = layui.layer;
                            layer.msg("属性" + app.new_key_name + "已存在，请使用其他属性名称", {icon: 2});
                        })
                    }else{
                        this.$emit("add_new_data", {src_type:"Object", key:this.new_key_name, item_type:this.new_type, stack:this.stack});
                    }
                }
            }
        },

        template: `
        <div class="layui-form layui-form-pane">
          <div class="layui-collapse" lay-accordion="" lay-filter="test">
            <div class="layui-colla-item">
              <h2 class="layui-colla-title">
              <span  @click="expand=!expand">[[ make_index_string(stack) ]]
              <i class="layui-icon layui-colla-icon">[[ expand?"":"" ]]</i>
              </span>
              </h2>
              <div class="layui-colla-content layui-show">
                <div v-if="get_data_type(current_data) == 'Object' || get_data_type(current_data) == 'Array'" v-show="expand">
                  <table class="layui-table" lay-size="sm">
                    <colgroup>
                      <col width="100">
                      <col>
                      <col width="50" v-if="dev">
                    </colgroup>
                    <thead>
                      <tr>
                        <th>索引</th>
                        <th>值</th>
                        <th v-if="dev">操作</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(value,key) in current_data">
                        <td>[[ key ]]</td>
                        <td><data_form :current_data=value :stack="add_item_to_array(stack, key)"
                                       @data_change="$emit('data_change', $event);" @delete_data="$emit('delete_data', $event)" @add_new_data="$emit('add_new_data', $event)" :dev="dev"></data_form></td>
                        <td >
                            <button v-if="dev" class="layui-btn layui-btn-danger layui-btn-sm"><i class="layui-icon" @click="$emit('delete_data', {stack:stack, index:key})" title="删除"></i></button>
                        </td>
                      </tr>
                      <tr v-if="dev && (get_data_type(current_data) == 'Object' || get_data_type(current_data) == 'Array')" >
                        <td>
                           <input type="text" v-if="dev && get_data_type(current_data) == 'Object'" v-model="new_key_name" placeholder="新属性名" class="layui-input">
                        </td>
                        <td>
                           <select class="layui-select" v-model="new_type">
                             <option value="Number">数字</option>
                             <option value="String">字符串</option>
                             <option value="Array">数组</option>
                             <option value="Object">对象</option>
                           </select>
                        </td>
                       <td>
                       <button class="layui-btn layui-btn-sm"><i class="layui-icon" title="新增" @click="add_new"></i></button>
                       </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div v-else-if="get_data_type(current_data) == 'String'" v-show="expand">
                    <div class="layui-form-item layui-form-text">
                        <div class="layui-input-block" v-show="single_line">
                            <input type="text" v-model="tmp_value" autocomplete="off" placeholder="请输入内容" class="layui-input">
                        </div>
                        <div class="layui-input-block" v-show="!single_line">
                            <textarea placeholder="请输入内容" v-model="tmp_value" class="layui-textarea"></textarea>
                        </div>
                    </div>
                    <button class="layui-btn layui-btn-radius layui-btn-sm" @click="single_line=!single_line">[[ single_line?"多行编辑":"单行编辑" ]]</button>
                    <button class="layui-btn layui-btn-normal layui-btn-radius layui-btn-sm"  @click="data_changed">确认修改</button>
                </div>
                <div v-else-if="get_data_type(current_data) == 'Number'" v-show="expand">
                    <div class="layui-form-item layui-form-text">
                        <div class="layui-input-inline">
                            <input type="number" name="phone" lay-verify="required|number" placeholder="请输入数字" autocomplete="off" class="layui-input" v-model="tmp_value">
                        </div>
                    </div>
                    <button class="layui-btn layui-btn-normal layui-btn-radius layui-btn-sm" @click="data_changed">确认修改</button>
                </div>
            </div>
          </div>
        </div>
      </div>`
    }
);


let app = new Vue({
    el: "#app",
    data: {
        title: "XXX后台管理系统",
        dev: true,
        type_data: {

        },
        user: {
            "name": "张三",
            "img": "http://tva1.sinaimg.cn/crop.0.0.118.118.180/5db11ff4gw1e77d3nqrv8j203b03cweg.jpg"
        },

        footer: "XXX 公司 版权所有",
        page_type: "data"
    },
    delimiters: ["[[", "]]"],
    components : {
        data_form : data_form
    },
    methods: {
        on_edit_data: function () {
            this.page_type = "data";
        },

        on_add_new_data: function(data){
            let v = this.type_data;
            for (let key of data.stack){
                v = v[key];
            }
            let value = null;
            if(data.item_type === "Number"){
                value = 0;
            }else if(data.item_type === "String"){
                value = "";
            }else if(data.item_type === "Array"){
                value = [];
            }else{
                value = {};
            }
            if (data.src_type === "Array") {
                Vue.push(v, value);
            }else if(data.src_type === "Object"){
                Vue.set(v, data.key, value);
            }
            layui.use('layer', function () {
                let layer = layui.layer;
                layer.msg("添加成功", {icon:1});
            });
        },

        on_data_change: function (data) {
            let v = this.type_data;
            for (let key of data.stack.slice(0, data.stack.length - 1)) {
                v = v[key];
            }
            let key = data.stack[data.stack.length - 1];

            layui.use('layer', function () {
                let layer = layui.layer;
                layer.confirm("确认将值 " + v[key] + " 更新为 " + data.value + " ?", {
                    btn: ['确认', '取消'] //按钮
                }, function () {
                    // TODO 向后台更新数据
                    Vue.set(v, key, data.value);
                    layer.msg('更新成功', {icon: 1});
                }, function () {
                });
            });
        },

        on_delete_data : function (data) {
            let v = this.type_data;
            for (let key of data.stack){
                v = v[key];
            }

            layui.use(['layer'], function () {
                var layer = layui.layer;
                layer.confirm("确认将 " + data.index + " 删除 ?", {
                    btn: ['确认', '取消'] //按钮
                }, function () {
                    // TODO 向后台删除数据
                    Vue.delete(v, data.index);
                    layer.msg('删除成功', {icon: 1});
                }, function () {
                });
            });
        },

        delete_type_dlg: function () {
            let app = this;
            this.delete_type = [];
            layui.use(['layer'], function () {
                let $ = layui.jquery;
                let layer = layui.layer;
                let that = this;
                app.hide_delete_type = false;
                layer.open({
                    type: 1 //此处以iframe举例
                    , title: '请选择要删除的类别'
                    , area: ['390px', '260px']
                    , shade: 0
                    , offset: [ 0,0 ]
                    , content: $('.delete_type')
                    , btn:["删除", "取消"]
                    , yes:function () {
                        alert(app.delete_type);
                    },
                    btn2: function () {

                    }
                });
            });
        },
    },
});

