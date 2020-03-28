
Vue.component("waveform", {
  props: [
    "playedWaveImage",
    "playingWaveImage",
    "time",
    "height"
  ],
  data: function() {
    return {
      width: 0
    };
  },
  mounted: function() {
    this.width = document.getElementById("playing-waveform").clientWidth;
  },
  computed: {
    widthFromTime: function() {
      return this.time * this.width;
    },
    waveformWrapperStyles: function() {
      return {
        position: "relative",
        height: this.height + "px"
      };
    },
    playedWaveImageWrapperStyles: function() {
      return {
        position: "absolute",
        top: "0px",
        left: "0px",
        width: (this.time * 100.0) + "%",
        height: this.height + "px",
        overflow: "hidden"
      };
    },
    playedWaveImageStyles: function() {
      return {
        position: "relative",
        top: "0px",
        left: "0px",
        width: this.width + "px",
        height: this.height + "px",
        zIndex: "1"
      };
    },
    playingWaveImageStyles: function() {
      return {
        backgroundImage: `url("${this.playingWaveImage}")`,
        backgroundSize: `100% ${this.height}px`,
        position: "absolute",
        top: "0px",
        left: "0px",
        width: "100%",
        height: this.height + "px",
        zIndex: "0"
      };
    }
  },
  methods: {
    onClick: function(event) {
      let clientRect = event.currentTarget.getBoundingClientRect();
      let x = event.clientX - clientRect.left;
      this.$emit("set-time", x / clientRect.width);
    }
  },
  template: `
    <div v-on:click="onClick" v-bind:style="waveformWrapperStyles">
      <div
        v-bind:style="playedWaveImageWrapperStyles">
        <img
          id="played-waveform"
          v-bind:src="playedWaveImage"
          v-bind:style="playedWaveImageStyles" />
      </div>
      <div
        id="playing-waveform"
        v-bind:style="playingWaveImageStyles" />
    </div>
  `
});

Vue.component("play-button", {
  props: ["playing"],
  methods: {
    onClick: function(event) {
      this.$emit("set-playing", !this.playing);
    }
  },
  template: `
    <button class="btn-real" v-on:click="onClick">
      <img v-bind:src="playing ? 'pause.svg' : 'play.svg'" style="width: 40px">
    </button>
  `
});

Vue.component("player-ui", {
  props: [
    "playing",
    "time",
    "playedWaveImage",
    "playingWaveImage",
    "title",
    "musicPageHref",
    "thumbnail"
  ],
  methods: {
    setPlaying: function(playing) {
      this.$emit("set-playing", playing);
    },
    setTime: function(time) {
      this.$emit("set-time", time);
    }
  },
  computed: {
    thumbnailStyle: function() {
      return {
        "background-image": `url("${this.thumbnail}")`
      };
    }
  },
  template: `
    <div class="player">
      <div
        class="thumbnail"
        v-bind:style="thumbnailStyle">
      </div>
      <div class="grid-right">
        <a
            class="music-title"
            v-bind:href="musicPageHref" >
          {{ title }}
        </a>
        <div class="playbtn-and-waveform">
          <div class="playbtn-bg">
            <play-button
              class="playbtn"
              v-bind:playing="playing"
              v-on:set-playing="setPlaying">
            </play-button>
          </div>
          <div>
            <waveform
              v-bind:played-wave-image="playedWaveImage"
              v-bind:playing-wave-image="playingWaveImage"
              v-bind:time="time"
              height="60"
              v-on:set-time="setTime">
            </waveform>
          </div>
        </div>
      </div>
    </div>
  `
});

Vue.component("player", {
  props: [
    "musicinfoUrl",  // musicinfo.jsonへのURL
    "playingIndex",  // 現在再生中のプレイヤー番号
    "indexInList"    // このプレイヤーのプレイヤー番号
  ],
  data: function() {
    return {
      id: null,
      title: null,
      duration: 0,
      waveformPlaying: null,
      waveformPlayed: null,
      thumbnail: null,
      hls: null,
      hlsInitialized: false,
      playing: false,
      time: 0.0
    };
  },
  mounted: function() {
    this.loadMusicInfo(this.musicinfoUrl);
  },
  beforeDestroy: function() {
    this.destroy();
  },
  methods: {
    initHLS: function() {
      return new Promise((resolve, reject) => {
        if( this.videoElem.canPlayType("application/vnd.apple.mpegurl") ) {
          // HLSにネイティブに対応しているならそっちを優先
          this.videoElem.src = this.src;
          this.videoElem.addEventListener("loadedmetadata", () => {
            this.hlsInitialized = true;
            resolve();
          });
        } else if( Hls.isSupported() ) {
          // ネイティブに対応していない場合はhls.jsを使用
          this.hls = new Hls();
          this.hls.loadSource(this.src);
          this.hls.attachMedia(this.videoElem);
          this.hls.on(Hls.Events.MANIFEST_PARSED, () => {
            this.hlsInitialized = true;
            resolve();
          });
        } else {
          // どっちもダメなら再生できない
          reject("This browser does not support HLS.");
        }
      });
    },
    destroy: function() {
      this.setPlaying(false);
      if( this.hls != null ) {
        this.hls.destroy();
        this.hls = null;
      }
      this.hlsInitialized = false;
    },
    loadMusicInfo: function(url) {
      this.fetchMusicinfo(url)
        .then((musicinfo) => {
          this.id = musicinfo["id"];
          this.title = musicinfo["title"];
          this.duration = musicinfo["duration"];
          this.waveformPlaying = musicinfo["waveformPlaying"];
          this.waveformPlayed = musicinfo["waveformPlayed"];
          this.src = musicinfo["playlistUrl"];
          this.thumbnail = musicinfo["thumbnail"];
          this.$emit("musicinfo-loaded", this.indexInList, musicinfo);
        }).catch((response) => {
          console.log(response);
          alert("Failed to load musicinfo: " + url);
        });
    },
    fetchMusicinfo: function(url) {
      return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest();
        xhr.addEventListener("loadend", (event) => {
          if( xhr.status === 200 || xhr.status === 304 ) {
            resolve(JSON.parse(xhr.responseText));
          } else {
            reject(xhr.response);
          }
        });
        xhr.open("GET", url);
        xhr.send(null);
      });
    },
    setPlaying: function(playing) {
      this.playing = playing;

      if( this.videoElem == null ) return;

      if( playing ) {
        if( this.hlsInitialized ) {
          this.videoElem.play();
          this.videoElem.currentTime = this.time * this.duration;
          this.$emit("start-playing", this.indexInList);
          this.timerLoop();
        } else {
          // HLSが初期化されていなかったときは初期化してから再生する
          this.initHLS()
            .then(() => {
              this.videoElem.play();
              this.videoElem.currentTime = this.time * this.duration;
              this.$emit("start-playing", this.indexInList);
              this.timerLoop();
            }).catch((message) => {
              alert(message);
            });
        }

        this.$emit("started-playing-callback", this.id, this.title);

      } else {
        this.videoElem.pause();
      }
    },
    setTime: function(time) {
      this.time = time;
      if( this.playing ) {
        this.videoElem.currentTime = this.time * this.duration;
      }
    },
    timerLoop: function() {
      if( !this.playing ) return;

      this.time = this.videoElem.currentTime / this.duration;
      if( 1.0 <= this.time ) {
        this.playing = false;
        this.time = 0.0;
        this.$emit("finished-playing", this.indexInList);
      } else {
        setTimeout(this.timerLoop, 100);
      }
    }
  },
  computed: {
    videoElemId: function() {
      return "vid-" + this.id;
    },
    videoElem: function() {
      return document.getElementById(this.videoElemId);
    },
    musicPageHref: function() {
      return "/music.html?id=" + this.id;
    }
  },
  watch: {
    musicinfoUrl: function(newUrl) {
      this.destroy();
      this.setTime(0.0);
      this.loadMusicInfo(newUrl);
    },
    playingIndex: function(newIndex) {
      if( this.indexInList !== newIndex ) {
        // 自分以外のプレイヤーの再生が始まったら自分のリソースを開放する
        this.destroy();
      } else if( this.indexInList === newIndex && !this.playing ) {
        // 自分のインデックスになった場合は再生を開始する
        this.setTime(0.0);
        this.setPlaying(true);
      }
    }
  },
  template: `
    <div>
      <video
        v-bind:id="videoElemId"
        style="display: none"
        playsinline></video>
      <player-ui
        class="player"
        v-bind:playing="playing"
        v-bind:time="time"
        v-bind:played-wave-image="waveformPlayed"
        v-bind:playing-wave-image="waveformPlaying"
        v-bind:title="title"
        v-bind:music-page-href="musicPageHref"
        v-bind:thumbnail="thumbnail"
        v-on:set-playing="setPlaying"
        v-on:set-time="setTime">
      </player-ui>
    </div>
  `
});

Vue.component("player-list", {
  props: ["musicinfoUrls"],
  data: function() {
    return {
      playingIndex: null
    }
  },
  methods: {
    musicinfoLoaded: function(index, musicinfo) {
      this.$emit("musicinfo-loaded", index, musicinfo);
    },
    startPlaying: function(index) {
      this.playingIndex = index;
    },
    finishedPlaying: function(index) {
      if( index === this.musicinfoUrls.length - 1 ) {
        // 最後のプレイヤーの再生が終了したら，すべてのプレイヤーの再生を止める
        this.playingIndex = null;
      } else {
        // プレイヤーの再生が終了したら，次のプレイヤーの再生を開始する
        this.playingIndex = this.playingIndex + 1;
      }
    },
    startedPlayingCallback: function(id, title) {
      this.$emit("started-playing-callback", id, title);
    }
  },
  template: `
    <div class="player-list">
      <player
        class="player-list-item"
        v-for="(music, index) in musicinfoUrls"
        v-bind:musicinfo-url="music"
        v-bind:playing-index="playingIndex"
        v-bind:index-in-list="index"
        v-on:musicinfo-loaded="musicinfoLoaded"
        v-on:start-playing="startPlaying"
        v-on:finished-playing="finishedPlaying"
        v-on:started-playing-callback="startedPlayingCallback">
      </player>
    </div>
  `
});

Vue.component("pager", {
  props: [
    "musics",
    "musicsPerPage"
  ],
  data: function() {
    return {
      "currentPage": 0
    };
  },
  methods: {
    onClickedNewerBtn: function(evt) {
      this.currentPage = Math.max(0, this.currentPage - 1);
      this.$emit("page-changed", this.currentPage, this.pagedMusics);
    },
    onClickedOlderBtn : function(evt) {
      this.currentPage = Math.min(this.currentPage + 1, this.maxPages);
      this.$emit("page-changed", this.currentPage, this.pagedMusics);
    }
  },
  computed: {
    maxPages: function() {
      return Math.floor(this.musics.length / this.musicsPerPage);
    },
    pagedMusics: function() {
      let start = this.musicsPerPage * this.currentPage;
      let end = Math.min(start + this.musicsPerPage, this.musics.length);
      return this.musics.slice(start, end);
    }
  },
  watch: {
    musics: function(newMusics) {
      Vue.nextTick(() => {
        this.currentPage = Math.max(0, Math.min(this.currentPage, this.maxPages));
        this.$emit("page-changed", this.currentPage, this.pagedMusics);
      });
    }
  },
  template: `
    <div class="pager">
      <button
          class="btn-pager"
          v-show="0 < currentPage"
          v-on:click="onClickedNewerBtn">
        ◀ 最近の曲へ
      </button>
      <button
          class="btn-pager"
          v-show="currentPage < maxPages"
          v-on:click="onClickedOlderBtn">
        昔の曲へ ▶
      </button>
    </div>
  `
});

Vue.component("search-box", {
  data: function() {
    return {
      searchText: ""
    };
  },
  watch: {
    searchText: function(newText) {
      this.$emit("updated-search-text", newText);
    }
  },
  template: `
    <div class="search-box">
      <i class="fas fa-search"></i>
      <input
        type="text"
        placeholder="曲名で検索"
        v-model="searchText">
    </div>
  `
});

