angular.module('memeApp', ['ngRoute'])
  .factory('memeFactory', ['$http', function($http) {

    var urlBase = '/api/v1/meme/';
    var memeFactory = {};

    // for getting memes to vote on
    memeFactory.getMeme = function() {
      return $http.get('/chilies/test');
    };

    // to add new memes to the db
    memeFactory.addNew = function(meme) {
      return $http.post(urlBase, meme);
    };

    // to save votes on memes
    memeFactory.memeVote = function(vote) {
      return $http.post('/api/v1/vote/?', vote);
    };
    
    return memeFactory;
  }])

  .controller('AddNewController', ['$scope', '$http', 'memeFactory', 
    function($scope, $http, memeFactory) {
    var self = this;

    // submits a new meme to tastypie
    self.submit = function() {
      memeFactory.addNew(self.meme)
        .success(function(response) {
          $scope.ctrl.meme.title='';
          $scope.ctrl.meme.image_url='';
          $scope.ctrl.msg = "Success! Add another!";  
        })
        .error(function(error) {
          console.log('post to api failed');
          $scope.ctrl.errorMsg = "Please login to add content.";
        });
    };
  }])

  .controller('MainController', ['$scope', 'memeFactory',
    function($scope, memeFactory) {

      var displayMemes = [];

      // Retrieves the meme data from memeFactory, if there is an error it reloads the page. 
      function getMemes() {
        memeFactory.getMeme()
          .success(function(data) {
            $scope.voteDisplay = true;
            $scope.memes = data;
            displayMemes = data;
          })
          .error(function(error) {
            console.log('getMemes failed to load');
          });
      }
      
      getMemes();

      $scope.vote = function() {
        // When clicked, determines the id of the winner and loser
        var winnerId = this.meme.id;
        if (displayMemes[0].id !== winnerId) {
          loserId = displayMemes[0].id;
        }
        else {
          loserId = displayMemes[1].id;
        }
        var vote = {winner: winnerId, loser: loserId};
        // vote is pushed to tastypie which upon succeeding delays before the next set is loaded
        memeFactory.memeVote(vote)
          .then(function(response) {
            // Display the score and after 2 seconds retrieve new memes
            $scope.voteDisplay=!$scope.voteDisplay;
            window.setTimeout(function() {
              getMemes();
            }, 2000);
          });
      }; 
    }])

  .controller('ImageController', ['$scope', function($scope) {

    $scope.slides = [
      {image: 'https://farm3.staticflickr.com/2342/2499955060_40491d5c76_b.jpg', description: 'Tasty ear'},
      {image: 'https://farm4.staticflickr.com/3245/2463696892_8098b24736_b.jpg', description: 'Food!'},
      {image: 'https://farm3.staticflickr.com/2324/2408531540_5669a42fe0_b.jpg', description: 'Bike war'},
      {image: 'https://farm3.staticflickr.com/2159/2449237472_6b7d1710f7_b.jpg', description: 'Safe'},
      {image: 'https://farm3.staticflickr.com/2169/2407909998_063e398b7c_b.jpg', description: 'The investigator'}
    ];
    // we want to start at the first slide
    $scope.currentIndex = 0;

    $scope.direction = 'left';

    // allows us to change which slide is seen by changing the index
    $scope.setCurrentSlideIndex = function(index) {
      $scope.direction = (index > $scope.currentIndex) ? 'left' : 'right';
      $scope.currentIndex = index;
    };

    // returns a boolean checking if the current index is the slide index we are on
    $scope.isCurrentSlideIndex = function(index) {
      return $scope.currentIndex === index;
    };

    $scope.previousSlide = function() {
      $scope.direction = 'left';
      $scope.currentIndex = ($scope.currentIndex < $scope.slides.length - 1) ? ++$scope.currentIndex : 0;
    };

    $scope.nextSlide = function() {
      $scope.direction = 'right';
      $scope.currentIndex = ($scope.currentIndex > 0) ? --$scope.currentIndex : $scope.slides.length - 1;
    };
  }])

  .config(['$routeProvider', function($routeProvider) {

    $routeProvider.when('/', {
      templateUrl: '/static/main.html',
      controller: 'MainController'
    })
    .when('/add', {
      templateUrl: '/static/add.html',
      controller: 'AddNewController'
    })
    .when('/about', {
      templateUrl: '/static/about.html',
      controller: 'ImageController'
    })
    .otherwise({redirectTo: '/'});
  }]);