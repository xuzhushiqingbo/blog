<template>
<Row>
  <Card class="content-box">
    <Row>
      <span>请选择编辑器类型：</span>
      <RadioGroup v-model="editorType">
        <Radio label="markdown">MarkDown编辑器</Radio>
        <Radio label="richeditor">富文本编辑器</Radio>
      </RadioGroup>
    </Row>
    <Divider>我撕故我在，请开始您的创作吧！</Divider>
    <Row class="editor" v-if="editorType==='markdown'">
        <!--<i-input v-model="formValidate.content" type="textarea" :autosize="{minRows: 10,maxRows: 35}" placeholder="请输入文章内容(markdown)..."></i-input>-->
        <mavon-editor ref=md v-model="editorContent" @change="handleMavonChange" @save="handleMavonSave"  @imgAdd="handleImgAdd1" @imgDel="handleImgDel"/>
    </Row>
    <Row class="editor" v-if="editorType==='richeditor'">
      <!--<i-input v-model="formValidate.content" type="textarea" :autosize="{minRows: 10,maxRows: 35}" placeholder="请输入文章内容(richeditor)..."></i-input>-->
      <quill-editor v-model="editorContent"
                    ref="myQuillEditor"
                    :options="editorOption"
                    @blur="onEditorBlur($event)"
                    @focus="onEditorFocus($event)"
                    @ready="onEditorReady($event)"
                    @change="onEditorChange($event)">
      </quill-editor>
    </Row>
  </Card>
  <Divider><h3>请填写文章的其他信息</h3></Divider>
  <Card class="info-box">
    <Row :gutter="16">
      <i-col span="6">
        <div style="width: 100%;height: 1px"></div>
      </i-col>
      <i-col span="12">
        <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
          <FormItem label="文章标题" prop="title">
            <Input v-model="formValidate.title" placeholder="请输入文章标题..."/>
          </FormItem>
          <FormItem label="文章分类" prop="category">
            <Select v-model="formValidate.category">
              <Option v-for="item in categories" :key="item.id" :value="item.id">{{item.name}}</Option>
            </Select>
          </FormItem>
          <FormItem label="文章标签" prop="tags">
            <Select v-model="formValidate.tags" multiple>
              <Option v-for="item in tags" :key="item.id" :value="item.id">{{item.name}}</Option>
            </Select>
          </FormItem>
          <FormItem label="文章简介" prop="brief">
            <Input v-model="formValidate.brief" type="textarea" :autosize="{minRows: 2,maxRows: 5}" placeholder="请输入20-120字内的简介..."/>
          </FormItem>
          <FormItem label="文章封面" prop="cover">
            <Upload :before-upload="handleBeforeUpload" action="/">
              <Button icon="ios-cloud-upload-outline">为文章选择封面图像</Button>
            </Upload>
            <p v-if="formValidate.cover !== null">上传的文件名:{{formValidate.cover.name}}</p>
          </FormItem>
          <FormItem>
           <Button type="primary" @click="handleSubmit('formValidate')">发布文章</Button>
            <Button @click="handleReset('formValidate')" style="margin-left: 8px">重置表单</Button>
            <Button @click="uploadimg()" style="margin-left: 8px">上传文章插图</Button>
          </FormItem>
        </Form>
      </i-col>
      <i-col span="6">
        <div style="width: 100%;height: 1px"></div>
      </i-col>
    </Row>
  </Card>
</Row>
</template>

<script>
import { mapGetters } from 'vuex'
import { getBlogCategories, getBlogTags, createArticle, createArticleImage, postArticleImage } from '../api/api'
// import axios from 'axios'

export default {
  name: 'BlogCreate',

  data () {
    return {
      categories: [],
      tags: [],
      taglimit: 1000,
      tagsCount: 0,
      editorType: 'markdown',
      editorContent: '',
      editorOption: {
        // some quill options
      },
      formValidate: {
        title: '',
        category: '',
        tags: [],
        cover: null,
        brief: '',
        content: ''
      },
      ruleValidate: {
        title: [
          { required: true, message: '文章标题不能为空', trigger: 'blur' }
        ],
        category: [
          { type: 'number', required: true, message: '分类是必填的', trigger: 'blur' }
        ],
        tags: [
          { type: 'array', required: true, message: '文章的分类标签是必填的', trigger: 'blur' }
        ],
        brief: [
          { required: true, message: '文章的简介是必填的', trigger: 'blur' },
          { type: 'string', min: 10, max: 120, message: '简介内容应在20到120个字之间', trigger: 'blur' }
        ]
      },
      img_file: {},
      img_pos: {}
    }
  },
  computed: {
    ...mapGetters(['userId']),
    quillEditor () {
      if (this.editorType === 'richeditor') {
        return this.$refs.myQuillEditor.quill
      } else {
        return null
      }
    }
  },
  methods: {
    handleMavonChange (value, render) {
      this.editorContent = value
      this.formValidate.content = render
    },
    handleMavonSave (value, render) {
      this.editorContent = value
      this.formValidate.content = render
    },
    // 绑定@imgAdd event
    handleImgAdd0 (pos, $file) {
      // 第一步.将图片上传到服务器.
      let formdata = new FormData()
      formdata.append('image', $file)
      createArticleImage(formdata).then((response) => {
        // 第二步.将返回的url替换到文本原位置![...](0) -> ![...](url)
        // console.log(response.data.image)
        // console.log(typeof (response.data.image))
        this.$refs.md.$img2Url(pos, response.data.image)
      })
    },
    handleImgAdd (pos, $file) {
      // 缓存图片信息
      this.img_file[pos] = $file
      this.img_pos[pos] = pos
    },
    handleImgDel (pos) {
      delete this.img_file[pos]
      delete this.img_pos[pos]
    },
    uploadimg () {
      // 第一步.将图片上传到服务器.
      for (let _img in this.img_file) {
        let formdata = new FormData()
        formdata.append('image', this.img_file[_img])
        createArticleImage(formdata).then((response) => {
          // 第二步.将返回的url替换到文本原位置![...](0) -> ![...](url)
          this.$refs.md.$img2Url(this.img_pos[_img], response.data.image)
        })
      }
    },
    // 绑定@imgAdd event
    handleImgAdd1 (pos, $file) {
      // 第一步.将图片上传到服务器.
      let formdata = new FormData()
      formdata.append('image', $file)
      postArticleImage(formdata).then((response) => {
        // 第二步.将返回的url替换到文本原位置![...](0) -> ![...](url)
        // console.log(response)
        // console.log(typeof (response.data))
        // console.log(response.data.split('{')[1].split('}')[0].split(':')[1])
        // console.log(response.data.image)
        // let respath = 'http://127.0.0.1:8000' + response.data.split('{')[1].split('}')[0].split(':')[1].split('"')[1]
        // console.log(respath)
        this.$refs['md'].$img2Url(pos, response.data.image)
      }).catch((error) => {
        console.log((error.response))
        if (error.response.status === 400) {
          alert(error.response.data.image)
        }
      })
    },
    onEditorBlur (quill) {
      console.log('editor blur!', quill)
    },
    onEditorFocus (quill) {
      console.log('editor focus!', quill)
    },
    onEditorReady (quill) {
      console.log('editor ready!', quill)
    },
    onEditorChange ({ quill, html, text }) {
      console.log('editor change!', quill, html, text)
      this.editorContent = html
      this.formValidate.content = html
    },
    obtainBlogCategories: function () {
      getBlogCategories({}).then(
        (response) => {
          this.categories = response.data
        }
      ).catch((error) => {
        console.log(error.response)
      })
    },
    obtainBlogTags: function (taglimit, tagoffset) {
      getBlogTags({ params: { limit: taglimit, offset: tagoffset } }).then(
        (response) => {
          this.tags = response.data.results
          this.tagsCount = response.data.count
        }
      ).catch((error) => {
        console.log(error.response)
      })
    },
    handleBeforeUpload (file) {
      this.formValidate.cover = file
      return false
    },
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          if (this.userId === '') {
            this.$Message.error('没有登录')
            return
          }
          if (this.formValidate.cover === null) {
            this.$Message.error('请选择封面图')
            return false
          }
          if (this.formValidate.content === null) {
            this.$Message.error('请书写文章内容')
            return false
          }
          let formDate = new FormData()
          formDate.append('user', this.userId)
          formDate.append('title', this.formValidate.title)
          formDate.append('brief', this.formValidate.brief)
          formDate.append('category', this.formValidate.category)
          formDate.append('cover', this.formValidate.cover)
          this.formValidate.tags.forEach((item) => {
            formDate.append('tags', item)
          })
          if (this.editorType === 'markdown') {
            formDate.append('content', this.formValidate.content)
          }
          if (this.editorType === 'richeditor') {
            formDate.append('content', this.formValidate.content)
          }
          createArticle(formDate).then((response) => {
            let article = response.data
            this.$router.push({ name: 'blog_detail', params: { aid: article.id, ctg: article.category.id } })
          })
        } else {
          alert('表单验证不通过')
        }
      }
      )
    },
    handleReset (name) {
      // this.$refs[name].resetFields()
      this.formValidate.title = ''
      this.formValidate.category = ''
      this.formValidate.tags = []
      this.formValidate.cover = null
      this.formValidate.brief = ''
    }
  },
  watch: {
    editorType () {
      setTimeout(() => {
        if (this.editorType === 'richeditor') {
          this.editorContent = '<h1 class="ql-align-center">\n' +
            '                          <span class="ql-font-serif" style="background-color: rgb(240, 102, 102); color: rgb(255, 255, 255);"> I am Example 1! </span>\n' +
            '                        </h1>\n' +
            '                        <p><br></p>\n' +
            '                        <p><span class="ql-font-serif">W Can a man still be brave if he\'s afraid? That is the only time a man can be brave. </span></p>\n' +
            '                        <p><br></p>\n' +
            '                        <p><strong class="ql-font-serif ql-size-large">Courage and folly is </strong><strong class="ql-font-serif ql-size-large" style="color: rgb(230, 0, 0);">always</strong><strong class="ql-font-serif ql-size-large"> just a fine line.</strong></p>\n' +
            '                        <p><br></p>\n' +
            '                        <p><u class="ql-font-serif">There is only one God, and his name is Death. And there is only one thing we say to Death: "Not today."</u></p>\n' +
            '                        <p><br></p>\n' +
            '                        <p><em class="ql-font-serif">Fear cuts deeper than swords.</em></p>\n' +
            '                        <p><br></p>\n' +
            '                        <pre class="ql-syntax" spellcheck="false">const a = 10;<br>const editorOption = { highlight: text => hljs.highlightAuto(text).value };</pre>\n' +
            '                        <p><br></p>\n' +
            '                        <p><span class="ql-font-serif">Every flight begins with a fall.</span></p>\n' +
            '                        <p><br></p>\n' +
            '                        <p><a href="https://surmon.me/" target="_blank" class="ql-font-serif ql-size-small" style="color: rgb(230, 0, 0);"><u>A ruler who hides behind paid executioners soon forgets what death is. </u></a></p>\n' +
            '                        <p><br></p>\n' +
            '                        <iframe class="ql-video ql-align-center" frameborder="0" allowfullscreen="true" src="https://www.youtube.com/embed/QHH3iSeDBLo?showinfo=0" height="238" width="560"></iframe>\n' +
            '                        <p><br></p>\n' +
            '                        <p><span class="ql-font-serif">Hear my words, and bear witness to my vow. Night gathers, and now my watch begins. It shall not end until my death. I shall take no wife, hold no lands, father no children. I shall wear no crowns and win no glory. I shall live and die at my post. I am the sword in the darkness. I am the watcher on the walls. I am the fire that burns against the cold, the light that brings the dawn, the horn that wakes the sleepers, the shield that guards the realms of men. I pledge my life and honor to the Night’s Watch, for this night and all the nights to come.</span></p>\n' +
            '                        <p><br></p>\n' +
            '                        <p><span class="ql-font-serif">We are born to suffer, to suffer can make us strong.</span></p>\n' +
            '                        <p><br></p>\n' +
            '                        <p><span class="ql-font-serif">The things we love destroy us every time.</span></p>'
        } else {
          this.editorContent = '## 二级标题'
        }
      }, 300)
    }
  },
  mounted () {
    this.obtainBlogCategories()
    this.obtainBlogTags(this.taglimit, 0)
  }
}
</script>

<style scoped>

</style>
